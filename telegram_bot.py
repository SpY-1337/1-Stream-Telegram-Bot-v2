from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from data_fetcher import get_data, get_stream_data, restart_stream
from utilities import format_dashboard_stats, format_servers_info, notify_if_license_inactive, notify_server_status
from config import telegram_chat_id, thresholds, enable_automatic_restart, response_timeout
from tenacity import retry, stop_after_attempt, wait_fixed
import asyncio
import queue

alert_queue = queue.Queue()
ignore_stream_ids = set()  # Set to store stream IDs that should not be alerted again
restart_counts = {}  # Dictionary to track restart counts

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the Server Dashboard Bot! Type /status to get the latest stats.")

async def send_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = get_data()

    if data:
        dashboard_stats = format_dashboard_stats(data["dashboard"])
        servers_info = format_servers_info(data["servers"])

        message = dashboard_stats + servers_info

        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="Markdown")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def send_telegram_message(context, message, reply_markup=None):
    return await context.bot.send_message(
        chat_id=telegram_chat_id,
        text=message,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def check_bitrate(context: ContextTypes.DEFAULT_TYPE) -> None:
    stream_data = get_stream_data()

    if stream_data:
        for stream in stream_data:
            if stream['id'] in ignore_stream_ids:
                continue

            bitrate_str = stream['stream_info']['bitrate']
            if 'Mbps' in bitrate_str:
                bitrate = float(bitrate_str.replace(' Mbps', ''))
                fps = int(stream['stream_info']['fps'])
                speed_str = stream['stream_info']['speed']
                try:
                    speed = float(speed_str.replace('x', ''))
                except ValueError:
                    speed = 0.0  # Default to 0 if speed is not a number

                alert_reasons = []
                if bitrate > thresholds["bitrate"]:
                    alert_reasons.append(f"bitrate ({bitrate_str}) exceeded {thresholds['bitrate']} Mbps")
                if fps > thresholds["fps"]:
                    alert_reasons.append(f"FPS ({fps}) exceeded {thresholds['fps']}")
                if speed > thresholds["speed"]:
                    alert_reasons.append(f"speed ({speed_str}) exceeded {thresholds['speed']}x")

                if alert_reasons:
                    reasons = ", ".join(alert_reasons)
                    message = (
                        f"⚠️ ⚠️ ⚠️ **Stream Alert!** ⚠️ ⚠️ ⚠️\n\n"
                        f"**Name**: {stream['name']}\n"
                        f"**ID**: {stream['id']}\n"
                        f"**Bitrate**: {bitrate_str}\n"
                        f"**FPS**: {stream['stream_info']['fps']}\n"
                        f"**Speed**: {speed_str}\n"
                        f"**Clients watching**: {stream['stats_per_server'][0]['clients']}\n\n"
                        f"The alert was triggered because the {reasons}.\n\n"
                        "Please investigate or restart the stream.\n\n"
                        "Would you like to restart the stream? Yes or No"
                    )

                    keyboard = [
                        [
                            InlineKeyboardButton("Yes", callback_data=f"restart:{stream['id']}"),
                            InlineKeyboardButton("No", callback_data=f"ignore:{stream['id']}")
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    alert_queue.put((message, reply_markup, stream['id'], stream))

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    action, stream_id = query.data.split(':')

    if action == "restart":
        response = restart_stream(stream_id)
        if response and response.status_code == 200:
            await query.edit_message_text(text=f"Stream {stream_id} has been restarted successfully.")
        else:
            await query.edit_message_text(text=f"Failed to restart stream {stream_id}. Please try again later.")
    elif action == "ignore":
        ignore_stream_ids.add(stream_id)  # Add to ignore list
        await query.edit_message_text(text=f"Stream {stream_id} will not be alerted again.")

async def process_alerts(context: ContextTypes.DEFAULT_TYPE) -> None:
    while not alert_queue.empty():
        message, reply_markup, stream_id, stream = alert_queue.get()

        try:
            sent_message = await send_telegram_message(context, message, reply_markup)
            if enable_automatic_restart:
                await asyncio.sleep(response_timeout)
                if stream_id not in ignore_stream_ids:
                    response = restart_stream(stream_id)
                    if response and response.status_code == 200:
                        restart_count = restart_counts.get(stream_id, 0) + 1
                        restart_counts[stream_id] = restart_count
                        await context.bot.delete_message(chat_id=telegram_chat_id, message_id=sent_message.message_id)
                        await context.bot.send_message(
                            chat_id=telegram_chat_id,
                            text=(
                                f"Stream automatically restarted due to no response ✅.\n\n"
                                f"Name: {stream['name']}\n"
                                f"ID: {stream_id}\n\n"  # Added extra newline here
                                f"The telegram bot has automatically restarted this {restart_count} times"
                            )
                        )
        except Exception as e:
            print(f"Failed to process alert for stream {stream_id}: {e}")
        finally:
            alert_queue.task_done()

async def poll_status(context: ContextTypes.DEFAULT_TYPE) -> None:
    await notify_if_license_inactive(context)
    await notify_server_status(context)
    await check_bitrate(context)
    await process_alerts(context)

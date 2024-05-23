import time
import queue
import asyncio
from telegram.ext import ContextTypes
from config import thresholds, response_timeout, enable_automatic_restart, telegram_chat_id
from data_fetcher import get_stream_data

alert_queue = queue.Queue()
alert_timestamps = {}
ignore_stream_ids = set()
restart_counts = {}

async def check_high_traffic(context: ContextTypes.DEFAULT_TYPE) -> None:
    stream_data = get_stream_data()

    if stream_data:
        current_time = time.time()
        for stream in stream_data:
            stream_id = stream['id']
            if stream_id in ignore_stream_ids:
                continue

            clients = sum(server['clients'] for server in stream['stats_per_server'])

            if stream_id in alert_timestamps:
                last_alert_time = alert_timestamps[stream_id]
                if current_time - last_alert_time < 3600:  # 1 hour cooldown
                    continue

            if clients > thresholds['clients']:
                alert_timestamps[stream_id] = current_time
                message = (
                    f"🙈 🙉 🙊 High Traffic Alert! 🙈 🙉 🙊\n\n"
                    f"**Name**: {stream['name']}\n"
                    f"**ID**: {stream_id}\n"
                    f"**Clients watching**: {clients}\n\n"
                    "Please make sure you have enough load balancers added to handle the traffic."
                )
                alert_queue.put((message, None, stream_id, stream))

            elif stream_id not in alert_timestamps or current_time - alert_timestamps[stream_id] >= 3600:
                alert_timestamps.pop(stream_id, None)  # Reset the alert timestamp if conditions no longer met

async def process_alerts(context: ContextTypes.DEFAULT_TYPE) -> None:
    while not alert_queue.empty():
        message, reply_markup, stream_id, stream = alert_queue.get()

        try:
            await context.bot.send_message(chat_id=telegram_chat_id, text=message, parse_mode="Markdown")
            await asyncio.sleep(5) 
        except Exception as e:
            print(f"Failed to process alert for stream {stream_id}: {e}")
        finally:
            alert_queue.task_done()

async def poll_traffic_status(context: ContextTypes.DEFAULT_TYPE) -> None:
    await check_high_traffic(context)
    await process_alerts(context)

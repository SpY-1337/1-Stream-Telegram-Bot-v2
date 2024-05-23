import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram_bot import start, send_report, poll_status, handle_response
from traffic_monitor import poll_traffic_status
from config import telegram_token

nest_asyncio.apply()

async def main():
    application = ApplicationBuilder().token(telegram_token).build()

    start_handler = CommandHandler("start", start)
    status_handler = CommandHandler("status", send_report)
    response_handler = CallbackQueryHandler(handle_response)

    application.add_handler(start_handler)
    application.add_handler(status_handler)
    application.add_handler(response_handler)

    job_queue = application.job_queue

    # Poll stream status every 10 minutes (600 seconds)
    job_queue.run_repeating(poll_status, interval=600, first=10)
    # Poll traffic status every 10 minutes (600 seconds), starting 20 seconds after start
    job_queue.run_repeating(poll_traffic_status, interval=600, first=20)

    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

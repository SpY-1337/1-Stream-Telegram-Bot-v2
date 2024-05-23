# 1-Stream-Telegram-Bot v2
1 Stream Control Panel API - Python Implementation

This Python implementation leverages the 1 Stream Control Panel API to log into your administrative panel and retrieve back-end statistics. The gathered data is then reported via the Telegram API.

This code serves as a foundational framework with potential for extensive feature enhancements in future versions.

# Features in v2

# 1. Login to Admin Panel

Logs into the 1 Stream Control Panel using provided credentials and retrieves a CSRF token.

# 2. Retrieve Dashboard Stats

Fetches dashboard statistics such as total connections, streams, users, and license status.

# 3. Retrieve Server Information

Fetches information about all servers, including health status, live streams, load averages, connected clients, and version.

# 4. Retrieve Stream Data

Fetches detailed information about each stream, including bitrate, FPS, speed, and clients connected.

# 5. Telegram Integration

Sends reports and alerts to a specified Telegram chat using the Telegram Bot API.

# 6. Bitrate Monitoring

Monitors stream bitrate, FPS, and speed against specified thresholds.

Sends alerts if thresholds are exceeded.

Includes a prompt to restart the stream via Telegram.

Optionally, automatically restarts the stream if no response is received within a configurable timeout.

# 7. High Traffic Monitoring

Monitors the number of clients connected to each stream.

Sends alerts if the number of clients exceeds a specified threshold.

Ensures alerts are not sent repeatedly within a short period.

Allows a 1-hour cooldown period before re-alerting for the same stream unless there's a significant increase in traffic.

# 8. Queue Management

Uses a queue system to manage alerts and avoid sending too many messages at once.

Adds a delay between sending alerts to avoid Telegram flood control.

# 9. Configuration Options

Provides a config.json file to set thresholds for bitrate, FPS, speed, and clients.

Configurable response timeout and automatic restart option.

# 10. Logging

Logs the status of streams, alerts sent, and errors encountered.

# Configuration

Settings Explanation

telegram_token: This is the API token for your Telegram bot. It allows the bot to authenticate and send messages on Telegram. You can obtain this token from the BotFather when you create a new bot on Telegram.

telegram_chat_id: This is the unique identifier for the Telegram chat where the bot will send its messages. It can be a user ID, group ID, or channel ID. You can get this by starting a chat with your bot and then using the Telegram API to retrieve your chat ID.

base_url: The base URL of your 1 Stream Control Panel. This URL is used as the starting point for all API requests to the control panel.

credentials:

username: The username for logging into your 1 Stream Control Panel.

password: The password for logging into your 1 Stream Control Panel.

thresholds: This section contains various thresholds for monitoring your streams.

bitrate: The maximum allowed bitrate for streams. If a stream exceeds this bitrate, an alert is triggered.

fps: The maximum allowed frames per second for streams. If a stream exceeds this FPS, an alert is triggered.

speed: The maximum allowed speed for streams. If a stream exceeds this speed, an alert is triggered.

clients: The maximum number of clients allowed to watch a stream. If a stream exceeds this number of clients, an alert is triggered.

client_increase_percentage: The percentage increase in the number of clients that will trigger an alert. This helps in identifying sudden spikes in traffic.

response_timeout: The amount of time (in seconds) the bot will wait for a response before automatically taking an action, such as restarting a stream. This is useful for handling cases where manual intervention is not possible.

enable_automatic_restart: A boolean value (true or false) that determines whether the bot should automatically restart streams when certain conditions are met, such as when no response is received within the specified timeout period.

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

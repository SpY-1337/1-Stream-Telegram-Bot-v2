from config import telegram_chat_id
import requests

# State to keep track of previous server statuses
prev_server_statuses = {}

def format_dashboard_stats(dashboard_stats):
    return (
        f"**Dashboard Stats**\n"
        f"- Total Connections: {dashboard_stats['connections']['total']}\n"
        f"- Total Streams: {dashboard_stats['streams']['total']}\n"
        f"- Total Users: {dashboard_stats['users']['total']}\n"
        f"- License Status: {dashboard_stats['license']['status']}\n"
        f"- License Product Name: {dashboard_stats['license']['product_name']}\n"
    )

def format_servers_info(servers_info):
    formatted_servers = "\n**Servers Info**\n"
    for server in servers_info:
        formatted_servers += (
            f"\n**{server['name']}**\n"
            f"- IP: {server['ip']}\n"
            f"- Domain: {server['domain']}\n"
            f"- Status: {server['health_status']}\n"
            f"- Live Streams: {server['live_streams']}\n"
            f"- Online Streams: {server['online_streams']}\n"
            f"- Load (1/5/15): {server['load_avg_1']}/{server['load_avg_5']}/{server['load_avg_15']}\n"
            f"- Connected Clients: {server['connected_clients']}\n"
            f"- Version: {server['version']}\n"
        )
    return formatted_servers

async def notify_if_license_inactive(context):
    from data_fetcher import get_data

    data = get_data()
    if data and data['dashboard']['license']['status'] != 'Active':
        await context.bot.send_message(
            chat_id=telegram_chat_id,
            text="⚠️ License status is not active! Please check immediately.",
            parse_mode="Markdown"
        )

async def notify_server_status(context):
    from data_fetcher import get_data
    global prev_server_statuses

    data = get_data()
    if data:
        servers = data["servers"]
        current_statuses = {}

        for server in servers:
            server_name = server['name']
            health_status = server['health_status']
            current_statuses[server_name] = health_status

            if server_name in prev_server_statuses and prev_server_statuses[server_name] != health_status:
                if health_status != "online":
                    await context.bot.send_message(
                        chat_id=telegram_chat_id,
                        text=f"⚠️ Server **{server_name}** is currently **{health_status}**.",
                        parse_mode="Markdown"
                    )
                elif health_status == "online":
                    await context.bot.send_message(
                        chat_id=telegram_chat_id,
                        text=f"✅ Server **{server_name}** is back **{health_status}**.",
                        parse_mode="Markdown"
                    )

        prev_server_statuses = current_statuses

def restart_stream(restart_url):
    response = requests.get(restart_url)
    return response

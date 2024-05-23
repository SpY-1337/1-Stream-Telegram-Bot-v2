import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

telegram_token = config["telegram_token"]
telegram_chat_id = config["telegram_chat_id"]
base_url = config["base_url"]
credentials = config["credentials"]

thresholds = config["thresholds"]
response_timeout = config["response_timeout"]
enable_automatic_restart = config["enable_automatic_restart"]

login_url = f"{base_url}/login"
dashboard_url = f"{base_url}/api/dashboard-stats"
servers_url = f"{base_url}/api/servers/index?with_external_servers=1&with_gpu_processes=0"
stream_data_url = f"{base_url}/api/stream/data?draw=2&search[regex]=false&format=paginated&show_status_details=true"

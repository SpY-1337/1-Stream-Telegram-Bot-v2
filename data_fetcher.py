import requests
from bs4 import BeautifulSoup
from config import login_url, dashboard_url, servers_url, stream_data_url, credentials, base_url
import time

session = requests.Session()
csrf_token = None

cached_stream_data = None
last_fetched_time = None
cache_duration = 300  # Cache duration in seconds (5 minutes)

def get_csrf_token(session):
    global csrf_token
    if not csrf_token:
        login_page = session.get(login_url)
        soup = BeautifulSoup(login_page.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '_token'})['value']
    return csrf_token

def login(session):
    global csrf_token
    credentials["_token"] = get_csrf_token(session)
    response = session.post(login_url, data=credentials)
    if response.ok and "dashboard" in response.url:
        print("Login successful!")
        return True
    else:
        print("Login failed.")
        print("Raw response:", response.text)
        return False

def get_data():
    if login(session):
        dashboard_response = session.get(dashboard_url)
        servers_response = session.get(servers_url)

        dashboard_data = dashboard_response.json() if dashboard_response.status_code == 200 else {}
        servers_data = servers_response.json() if servers_response.status_code == 200 else []

        return {"dashboard": dashboard_data, "servers": servers_data}
    return None

def get_stream_data():
    global cached_stream_data, last_fetched_time

    current_time = time.time()
    if cached_stream_data and last_fetched_time and (current_time - last_fetched_time < cache_duration):
        return cached_stream_data

    if login(session):
        stream_response = session.get(stream_data_url)

        if stream_response.status_code == 200:
            stream_data = stream_response.json()
            cached_stream_data = stream_data['data']
            last_fetched_time = current_time
            return cached_stream_data
        else:
            print(f"Error: Unable to retrieve stream data, status code {stream_response.status_code}")
            return None
    return None

def restart_stream(stream_id):
    if login(session):
        csrf_token = get_csrf_token(session)
        restart_url = f"{base_url}/stream/{stream_id}/restart"
        headers = {
            'X-CSRF-TOKEN': csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f"{base_url}/streams"
        }
        response = session.post(restart_url, headers=headers)
        return response
    return None

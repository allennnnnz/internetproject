# line_notification.py

import requests
from line_notify_lib.config import Decard_TOKEN, Internetcenter_TOKEN, Chat_room_TOKEN
def send_line_notification(message,TOKEN):
    notify_url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': TOKEN
    }

    payload = {
        'message': message
    }

    response = requests.post(notify_url, headers=headers, data=payload)
    return response.text

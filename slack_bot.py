from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Token exists: %s", "SLACK_BOT_TOKEN" in os.environ)

# Initialize Slack app
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Add conversation store
app.client.conversations_store = {}

# Excel file path
EXCEL_PATH = "habit_journal_tracker.xlsx"

def save_response(date, day_number, status, thoughts):
    # Save to Excel
    try:
        df = pd.read_excel(EXCEL_PATH)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['date', 'day_number', 'status', 'thoughts'])
    
    new_row = pd.DataFrame({
        'date': [date],
        'day_number': [day_number],
        'status': [status],
        'thoughts': [thoughts]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(EXCEL_PATH, index=False)

@app.message("start")
def handle_start(message, say):
    logger.info(f"Received start message from user {message['user']} on platform {message.get('platform', 'unknown')}")
    say("Did you write 1 Article / 10 DMs / 1 Project? (yes/no)")

@app.message("yes|no")
def handle_status(message, say):
    logger.info(f"Received status message from user {message['user']}: {message['text']}")
    status = message['text'].lower()
    say("Please share a few thoughts about today:")
    app.client.conversations_store[message['user']] = {'status': status}

@app.message()
def handle_thoughts(message, say):
    if message['user'] in app.client.conversations_store:
        logger.info(f"Received thoughts message from user {message['user']}: {message['text']}")
        status = app.client.conversations_store[message['user']]['status']
        thoughts = message['text']
        
        today = datetime.now()
        date_str = today.strftime('%Y-%m-%d')
        day_number = today.timetuple().tm_yday
        
        save_response(date_str, day_number, status, thoughts)
        
        say("Thank you! Your response has been recorded.")
        del app.client.conversations_store[message['user']]
    else:
        logger.info(f"Received unexpected message from user {message['user']}: {message['text']}")
        say("Please start the conversation by typing 'start'")

if __name__ == "__main__":
    logger.info("Starting Slack bot...")
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start() 


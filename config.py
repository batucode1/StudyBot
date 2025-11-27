import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("ERROR: .env file not found or BOT_TOKEN is missing.!")
    exit()

TASK_NAME, TASK_DEADLINE, TASK_PRIORITY = range(3)
STUDY_SESSION = range(3, 4)
NOTE_TITLE, NOTE_CONTENT = range(4, 6)

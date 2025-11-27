
#  TELEGRAM STUDY BOT - PROJECT README


This project is a Python Telegram bot developed to help students track their 
daily tasks, record study sessions, and manage their lecture notes efficiently.


## INSTALLATION AND SETUP
--------------------------------------------
Follow these steps in order to run the bot on your local machine.

### 1. CREATE A TELEGRAM BOT
First, you need to create a bot on Telegram and obtain an API Token:

1. Open the Telegram app and search for "@BotFather".
2. Start the chat and send the command: /newbot
3. Assign a Name and a Username to your bot (Username must end with 'bot').
4. BotFather will give you an HTTP API Token (e.g., 123456:ABC-DEF...).
   >> COPY THIS TOKEN. <<




### 2. SET UP VIRTUAL ENVIRONMENT
Create a virtual environment to prevent dependencies from affecting your global system.

[For Mac/Linux]:
    python3 -m venv .venv
    source .venv/bin/activate

[For Windows]:
    python -m venv .venv
    .venv\Scripts\activate


### 3. INSTALL REQUIRED LIBRARIES
Install the necessary libraries for the project to run:

    pip install -r requirements.txt

(Note: If you do not have a requirements.txt file, run the following command instead):
    pip install python-telegram-bot==13.15 urllib3==1.26.18 python-dotenv


### 4. CREATE .env FILE (IMPORTANT!)
For security reasons, the API Token should not be hardcoded into the script.

1. Create a new file named ".env" inside the project folder.
2. Add the following line and replace the placeholder with your token:

    TELEGRAM_BOT_TOKEN=123456789:AAFw... (Paste Your Token Here)


### 5. RUN THE BOT
Everything is ready! Now you can start the bot from the terminal:

    python main.py

When you see the message "Bot running..." in the terminal, your bot is active.


## COMMAND LIST
--------------------------------------------
You can use the following commands in the Telegram chat:

/start            -> Starts the bot and shows the welcome message.

/addtask          -> Starts the wizard to add a new task.

/tasks            -> Lists your saved tasks.

/complete <ID>    -> Completes the task with the specified ID (e.g., /complete 1).

/study            -> Starts a study session and records the duration.

/stats            -> Shows total study time and statistics.

/addnote          -> Adds a new note.

/notes            -> Lists all your notes.

/search <keyword> -> Searches for a keyword within your notes.

/motivation       -> Sends a random motivational quote.

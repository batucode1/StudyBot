import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from datetime import datetime, timedelta
from config import TASK_NAME, TASK_DEADLINE, TASK_PRIORITY, STUDY_SESSION, NOTE_TITLE, NOTE_CONTENT
from database import user_data, save_data, initialize_user


def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    initialize_user(user_id)
    update.message.reply_text(
        "Welcome to Study Bot!\n\n"
        "Commands:\n"
        " /addtask - Add task\n"
        " /tasks - View tasks\n"
        " /complete [ID] - Complete task\n"
        "️ /study - Start study session\n"
        " /stats - View statistics\n"
        " /addnote - Add note\n"
        " /notes - View notes\n"
        " /search [keyword] - Search notes\n"
        " /motivation - Get motivation"
    )


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('The transaction has been canceled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def get_motivation(update: Update, context: CallbackContext):
    quotes = [
        "Success is the sum of small efforts, repeated day in and day out.",
        "The future belongs to those who prepare for it today.",
        "Don't be afraid of making mistakes, be afraid of not trying.",
        "An hour of work is worth more than an hour of dreaming."
    ]
    update.message.reply_text(f"{random.choice(quotes)}")


def add_task_start(update: Update, context: CallbackContext):
    update.message.reply_text("Let's add a task. What is the name of the task??")
    return TASK_NAME


def get_task_name(update: Update, context: CallbackContext):
    task_name = update.message.text
    if len(task_name) < 3:
        update.message.reply_text("The task name is too short! Enter at least 3 characters..")
        return TASK_NAME

    context.user_data['task_name'] = task_name

    reply_keyboard = [['Today', 'Tomorrow'], ['3 days', '1 week']]
    update.message.reply_text(
        "When is the deadline?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TASK_DEADLINE


def get_task_deadline(update: Update, context: CallbackContext):
    choice = update.message.text
    today = datetime.now()

    if 'Today' in choice:
        deadline = today.strftime("%Y-%m-%d")
    elif 'Tomorrow' in choice:
        deadline = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif '3 days' in choice:
        deadline = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    elif '1 week' in choice:
        deadline = (today + timedelta(days=7)).strftime("%Y-%m-%d")
    else:
        deadline = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    context.user_data['task_deadline'] = deadline

    reply_keyboard = [['High', 'Medium', 'Low']]
    update.message.reply_text(
        f"Date: {deadline}. What is the priority?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TASK_PRIORITY


def get_task_priority(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    priority = update.message.text.split()[-1]

    task = {
        "name": context.user_data['task_name'],
        "deadline": context.user_data['task_deadline'],
        "priority": priority,
        "completed": False,
        "id": len(user_data[user_id]["tasks"]) + 1
    }

    user_data[user_id]["tasks"].append(task)
    save_data()

    update.message.reply_text(f"Task added: {task['name']}", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def view_tasks(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    initialize_user(user_id)
    tasks = user_data[user_id]["tasks"]

    if len(tasks) == 0:
        update.message.reply_text("No tasks yet.")
        return

    message = "**Your Tasks:**\n\n"
    for task in tasks:
        status = "[✓]" if task['completed'] else "[ ]"
        message += f"{status} #{task['id']} - {task['name']} ({task['priority']})\n"

    update.message.reply_text(message)


def complete_task(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    initialize_user(user_id)

    if not context.args:
        update.message.reply_text("Usage: /complete [ID] (Example: /complete 1)")
        return

    try:
        task_id = int(context.args[0])
    except:
        update.message.reply_text("Geçersiz ID!")
        return

    tasks = user_data[user_id]["tasks"]
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_data()
            update.message.reply_text(f"Congratulations! Task completed: {task['name']}")
            return

    update.message.reply_text("No task was found with this ID.")


def start_study(update: Update, context: CallbackContext):
    reply_keyboard = [['25 min', '45 min'], ['60 min', '90 min']]
    update.message.reply_text(
        "How much do you want to work?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return STUDY_SESSION


def record_study_session(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    choice = update.message.text

    if '25' in choice:
        minutes = 25
    elif '45' in choice:
        minutes = 45
    elif '60' in choice:
        minutes = 60
    elif '90' in choice:
        minutes = 90
    else:
        minutes = 30

    session = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "duration_minutes": minutes
    }

    user_data[user_id]["study_sessions"].append(session)

    user_data[user_id]["total_study_minutes"] += minutes
    save_data()

    update.message.reply_text(f"{minutes} minutes saved!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def show_stats(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    initialize_user(user_id)
    sessions = user_data[user_id]["study_sessions"]

    if len(sessions) == 0:
        update.message.reply_text("No study record yet. /start with study!")
        return

    total_minutes = user_data[user_id]["total_study_minutes"]
    total_sessions = len(sessions)

    average_minutes = total_minutes / total_sessions

    longest = 0
    for session in sessions:
        if session['duration_minutes'] > longest:
            longest = session['duration_minutes']

    update.message.reply_text(
        f"**Statistics**\n\n"
        f"Total Work: {total_minutes} min\n"
        f"Session Count: {total_sessions}\n"
        f"Average Duration: {average_minutes:.1f} min\n"
        f"Longest Session: {longest} min"
    )


def add_note_start(update: Update, context: CallbackContext):
    update.message.reply_text("What should the note title be??")
    return NOTE_TITLE


def get_note_title(update: Update, context: CallbackContext):
    title = update.message.text
    if len(title) < 2:
        update.message.reply_text("The title is too short!")
        return NOTE_TITLE

    context.user_data['note_title'] = title
    update.message.reply_text("You can write the content of the note:")
    return NOTE_CONTENT


def get_note_content(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    content = update.message.text

    note = {
        "title": context.user_data['note_title'],
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "id": len(user_data[user_id]["notes"]) + 1
    }

    user_data[user_id]["notes"].append(note)
    save_data()

    update.message.reply_text("Note saved!")
    return ConversationHandler.END


def view_notes(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    initialize_user(user_id)
    notes = user_data[user_id]["notes"]

    if not notes:
        update.message.reply_text("You have no notes.")
        return

    message = "**Your Notes:**\n\n"
    for note in notes:
        message += f"📌 {note['title']}\n{note['content']}\n---\n"
    update.message.reply_text(message)


def search_notes(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    initialize_user(user_id)

    if not context.args:
        update.message.reply_text("Usage: /search [word]")
        return

    keyword = ' '.join(context.args).lower()

    notes = user_data[user_id]["notes"]
    found = []

    for note in notes:
        if keyword in note['title'].lower() or keyword in note['content'].lower():
            found.append(note)

    if not found:
        update.message.reply_text("No response found.")
    else:
        message = f"results for '{keyword}' :\n\n"
        for note in found:
            message += f"📌 {note['title']}\n{note['content']}\n---\n"
        update.message.reply_text(message)

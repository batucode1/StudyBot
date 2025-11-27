from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from config import TOKEN, TASK_NAME, TASK_DEADLINE, TASK_PRIORITY, STUDY_SESSION, NOTE_TITLE, NOTE_CONTENT
from database import load_data
import handlers


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    task_conv = ConversationHandler(
        entry_points=[CommandHandler('addtask', handlers.add_task_start)],
        states={
            TASK_NAME: [MessageHandler(Filters.text & ~Filters.command, handlers.get_task_name)],
            TASK_DEADLINE: [MessageHandler(Filters.text & ~Filters.command, handlers.get_task_deadline)],
            TASK_PRIORITY: [MessageHandler(Filters.text & ~Filters.command, handlers.get_task_priority)],
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel)]
    )

    study_conv = ConversationHandler(
        entry_points=[CommandHandler('study', handlers.start_study)],
        states={
            STUDY_SESSION: [MessageHandler(Filters.text & ~Filters.command, handlers.record_study_session)]
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel)]
    )

    note_conv = ConversationHandler(
        entry_points=[CommandHandler('addnote', handlers.add_note_start)],
        states={
            NOTE_TITLE: [MessageHandler(Filters.text & ~Filters.command, handlers.get_note_title)],
            NOTE_CONTENT: [MessageHandler(Filters.text & ~Filters.command, handlers.get_note_content)],
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel)]
    )

    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(CommandHandler("tasks", handlers.view_tasks))
    dp.add_handler(CommandHandler("complete", handlers.complete_task))
    dp.add_handler(CommandHandler("stats", handlers.show_stats))
    dp.add_handler(CommandHandler("notes", handlers.view_notes))
    dp.add_handler(CommandHandler("search", handlers.search_notes))
    dp.add_handler(CommandHandler("motivation", handlers.get_motivation))

    dp.add_handler(task_conv)
    dp.add_handler(study_conv)
    dp.add_handler(note_conv)

    print("Bot running...")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    load_data()
    main()

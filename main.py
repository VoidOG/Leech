import os
import mimetypes
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from xhamster_downloader import download_xhamster  # Make sure this is correctly imported
from config import BOT_TOKEN, LOG_GROUP_ID, UPLOAD_GROUPS, AUTHORIZED_USERS, VPS_LOG_FILE

# Initialize the bot
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def log_message(message):
    """Send log message to the log group and write to VPS log file."""
    updater.bot.send_message(chat_id=LOG_GROUP_ID, text=message)

    # Log to the VPS log file
    with open(VPS_LOG_FILE, 'a') as vps_log:
        vps_log.write(message + '\n')

def is_authorized(user_id):
    """Check if the user is authorized to use the bot."""
    return user_id in AUTHORIZED_USERS

def start(update, context):
    """Send a welcome message."""
    welcome_message = "Welcome to the leech bot! Use /help to see available commands."
    update.message.reply_text(welcome_message)

def help_command(update, context):
    """Display help message with available commands."""
    help_message = (
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/download [link] [name] - Download media from a link and save it with the specified name.\n"
        "/status - Get the current status of the bot.\n"
        "/logs - View recent logs of bot activities.\n"
        "/settings - Show current bot settings.\n"
        "/authorize [user_id] - Add a user to the authorized list.\n"
        "/deauthorize [user_id] - Remove a user from the authorized list.\n"
        "/restart - Restart the bot.\n"
        "/stats - Show bot statistics."
    )
    update.message.reply_text(help_message)

def download_command(update, context):
    """Handles the download command with optional file name."""
    if update.message:  # Ensure the message object exists
        if len(context.args) < 1:
            update.message.reply_text("Please provide a link to download.")
            return

        link = context.args[0]
        file_name = context.args[1] if len(context.args) > 1 else 'downloaded_file'

        try:
            # Example: download from XHamster
            file_path = download_xhamster(link, file_name)
            update.message.reply_text(f"Downloaded: {file_path}")

            # Log the download activity
            log_message(f"Downloaded: {link} -> {file_path}")
            
            # Upload the downloaded file to specified groups/channels
            upload_file_to_groups(file_path)
        except Exception as e:
            update.message.reply_text(f"Error occurred: {str(e)}")
            log_message(f"Error downloading: {link} - {str(e)}")
    else:
        print(f"Update has no message object: {update}")

def upload_file_to_groups(file_path):
    """Upload the downloaded file to specified groups/channels in its original format."""
    # Get the MIME type of the file
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type:
        if mime_type.startswith('video/'):
            send_func = updater.bot.send_video
        elif mime_type.startswith('audio/'):
            send_func = updater.bot.send_audio
        elif mime_type.startswith('image/'):
            send_func = updater.bot.send_photo
        elif mime_type.startswith('application/pdf'):
            send_func = updater.bot.send_document
        elif mime_type.startswith('application/'):
            # This will cover documents such as Word, Excel, etc.
            send_func = updater.bot.send_document
        else:
            send_func = updater.bot.send_document
    else:
        # If MIME type is unknown, default to sending as a document
        send_func = updater.bot.send_document

    # Loop through the list of groups and send the file
    for group_id in UPLOAD_GROUPS:
        try:
            with open(file_path, 'rb') as file:
                if send_func == updater.bot.send_video:
                    # If it's a video, send as a video
                    updater.bot.send_video(chat_id=group_id, video=file, supports_streaming=True)
                elif send_func == updater.bot.send_audio:
                    # If it's an audio file, send as audio
                    updater.bot.send_audio(chat_id=group_id, audio=file)
                elif send_func == updater.bot.send_photo:
                    # If it's an image, send as photo
                    updater.bot.send_photo(chat_id=group_id, photo=file)
                elif send_func == updater.bot.send_document:
                    # If it's a document (PDF, other docs), send as document
                    updater.bot.send_document(chat_id=group_id, document=file)
                    
                log_message(f"Uploaded {file_path} to group/channel ID: {group_id}")
        except Exception as e:
            log_message(f"Error uploading to {group_id}: {str(e)}")

def status(update, context):
    """Provides the current status of the bot."""
    status_message = "The bot is online and ready to assist you!"
    update.message.reply_text(status_message)

def logs(update, context):
    """Displays VPS logs."""
    try:
        with open(VPS_LOG_FILE, 'r') as vps_log:
            log_content = vps_log.read()
            update.message.reply_text(log_content)
    except Exception as e:
        update.message.reply_text(f"Error reading logs: {str(e)}")

def settings(update, context):
    """Displays the current bot settings."""
    settings_message = (
        "Authorized Users: " + ', '.join(AUTHORIZED_USERS) + "\n" +
        "Upload Groups: " + ', '.join(UPLOAD_GROUPS)
    )
    update.message.reply_text(settings_message)

def authorize(update, context):
    """Adds a user to the authorized list."""
    if len(context.args) != 1:
        update.message.reply_text("Usage: /authorize [user_id]")
        return

    user_id = context.args[0]
    if user_id not in AUTHORIZED_USERS:
        AUTHORIZED_USERS.append(user_id)
        update.message.reply_text(f"User {user_id} has been authorized.")
    else:
        update.message.reply_text(f"User {user_id} is already authorized.")

def deauthorize(update, context):
    """Removes a user from the authorized list."""
    if len(context.args) != 1:
        update.message.reply_text("Usage: /deauthorize [user_id]")
        return

    user_id = context.args[0]
    if user_id in AUTHORIZED_USERS:
        AUTHORIZED_USERS.remove(user_id)
        update.message.reply_text(f"User {user_id} has been deauthorized.")
    else:
        update.message.reply_text(f"User {user_id} is not authorized.")

def restart(update, context):
    """Restarts the bot."""
    update.message.reply_text("Restarting the bot...")
    os.execv(sys.executable, ['python'] + sys.argv)

def stats(update, context):
    """Displays statistics about the bot."""
    stats_message = (
        "Bot Statistics:\n"
        f"Authorized Users: {len(AUTHORIZED_USERS)}\n"
        f"Upload Groups: {len(UPLOAD_GROUPS)}"
    )
    update.message.reply_text(stats_message)

# Command handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('download', download_command))
dispatcher.add_handler(CommandHandler('status', status))
dispatcher.add_handler(CommandHandler('logs', logs))
dispatcher.add_handler(CommandHandler('settings', settings))
dispatcher.add_handler(CommandHandler('authorize', authorize))
dispatcher.add_handler(CommandHandler('deauthorize', deauthorize))
dispatcher.add_handler(CommandHandler('restart', restart))
dispatcher.add_handler(CommandHandler('stats', stats))

# Start the bot
updater.start_polling()
updater.idle()

import telebot
import os
from concurrent.futures import ThreadPoolExecutor
from youtube_downloader import download_youtube
from instagram_downloader import download_instagram
from google_drive_downloader import download_google_drive
from mediafire_downloader import download_mediafire

# Bot token
BOT_TOKEN = '7488772903:AAGP-ZvbH7K2XzYG9vv-jIsA12iRxTeya3U'
bot = telebot.TeleBot(BOT_TOKEN)

# List to store multiple group and channel IDs (numeric IDs only)
GROUP_CHANNEL_IDS = [
    -1001234567890,  # Replace with your first group ID
    -1009876543210   # Replace with your second group ID
]

# List of admin user IDs allowed to use the bot
ADMIN_USER_IDS = [
    123456789,  # Replace with actual admin user ID
    987654321   # Add more admin user IDs as needed
]

# ThreadPoolExecutor for managing multiple downloads concurrently
executor = ThreadPoolExecutor(max_workers=5)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id in ADMIN_USER_IDS:
        welcome_msg = (
            "Welcome to the Leech Bot! \n"
            "Send me a link from YouTube, Instagram, Google Drive, or Mediafire and I'll download it for you.\n"
            "/help - View commands.\n"
            "/stats - Get download statistics.\n"
            "/add_group - Add a group to upload files.\n"
            "/remove_group - Remove a group from uploading files.\n"
        )
        bot.send_message(message.chat.id, welcome_msg)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")
        return

    link = message.text.strip()

    if "youtube.com" in link or "youtu.be" in link:
        executor.submit(download_and_upload, download_youtube, link, message)
    elif "instagram.com" in link:
        executor.submit(download_and_upload, download_instagram, link, message)
    elif "drive.google.com" in link:
        executor.submit(download_and_upload, download_google_drive, link, message)
    elif "mediafire.com" in link:
        executor.submit(download_and_upload, download_mediafire, link, message)
    else:
        bot.send_message(message.chat.id, "Unsupported link format. Please provide a valid YouTube, Instagram, Google Drive, or Mediafire link.")

def download_and_upload(download_func, link, message):
    file_path = download_func(link)
    if isinstance(file_path, str) and os.path.exists(file_path):
        bot.send_message(message.chat.id, f"Download complete: {file_path}")
        bot.send_document(message.chat.id, open(file_path, 'rb'))
        upload_to_multiple_locations(file_path)
    else:
        bot.send_message(message.chat.id, file_path)  # Send the error message

def upload_to_multiple_locations(file_path):
    try:
        for chat_id in GROUP_CHANNEL_IDS:
            bot.send_message(chat_id, "Uploading file...")
            bot.send_document(chat_id, open(file_path, 'rb'))
    except Exception as e:
        print(f"Error uploading to {chat_id}: {e}")

# Run the bot
if __name__ == "__main__":
    bot.polling()

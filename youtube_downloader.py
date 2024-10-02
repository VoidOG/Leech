from pytube import YouTube
import os

def download_youtube(link,file_name):
    try:
        yt = YouTube(link)

        # Get the highest resolution stream available
        video_stream = yt.streams.get_highest_resolution()

        # Define the download path
        download_path = "downloads"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Download the video
        file_path = video_stream.download(output_path=download_path)

        return file_path  # Return the path to the downloaded file
    except Exception as e:
        return f"Error downloading video: {str(e)}"

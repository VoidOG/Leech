import yt_dlp
import os

def download_youtube(link, file_name=None):
    try:
        download_path = "downloads"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s') if not file_name else os.path.join(download_path, file_name + '.%(ext)s')
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            file_path = ydl.prepare_filename(info)  
            
        return file_path  
    except Exception as e:
        return f"Error downloading video: {str(e)}"

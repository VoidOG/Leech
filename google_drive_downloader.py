import gdown
import os

def download_google_drive(link):
    try:
        # Extract the file ID from the link
        file_id = link.split('/')[-2]
        
        # Define the download path
        download_path = "downloads"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Construct the download URL
        download_url = f"https://drive.google.com/uc?id={file_id}"

        # Define the output file path
        output_file_path = os.path.join(download_path, f"{file_id}.file")  # You can change the extension based on the file type

        # Download the file
        gdown.download(download_url, output_file_path, quiet=False)

        return output_file_path  # Return the path to the downloaded file
    except Exception as e:
        return f"Error downloading from Google Drive: {str(e)}"

import os

def download_xhamster(link, file_name):
    try:
        # Ensure the 'download/' directory exists
        download_path = 'download'
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Simulate downloading the file
        with open(f'{download_path}/{file_name}', 'wb') as f:
            f.write(b'Dummy file content')  # Placeholder content for the file

        return f"{download_path}/{file_name}"
    except Exception as e:
        raise FileNotFoundError(f"Error downloading file: {str(e)}")

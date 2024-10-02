from mega import Mega

def download_mega(link, file_name=None):
    """Download file from Mega.nz."""
    mega = Mega()
    m = mega.login()  # Log in anonymously
    file = mega.get_public_file(link)
    
    # Specify the filename if provided, otherwise use the original filename
    if file_name is None:
        file_name = file.name

    mega.download(file, dest_dir='download', dest_filename=file_name)
    return f'download/{file_name}' 

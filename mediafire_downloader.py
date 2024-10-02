import requests
from bs4 import BeautifulSoup

def download_mediafire(link, file_name=None):
    """Download file from Mediafire given a link and optional file name."""
    # Retrieve the download page
    response = requests.get(link)
    if response.status_code != 200:
        raise Exception("Failed to access Mediafire link.")

    # Parse the HTML to find the download link
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the download button in the HTML
    download_button = soup.find('a', {'id': 'downloadButton'})
    if not download_button:
        raise Exception("Download link not found.")

    download_link = download_button['href']
    
    # Get the actual download link
    download_response = requests.get(download_link)
    if download_response.status_code != 200:
        raise Exception("Failed to retrieve the file.")

    # Set the file name if not provided
    if file_name is None:
        # Extract the file name from the URL or use a default name
        file_name = link.split('/')[-1] + '.file'  # Change the extension as needed

    # Save the file
    with open(file_name, 'wb') as f:
        f.write(download_response.content)

    return file_name

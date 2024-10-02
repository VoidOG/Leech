import requests
from bs4 import BeautifulSoup

def download_pornhub(video_url, file_name=None):
    """Download video from Pornhub."""
    response = requests.get(video_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    video_source = soup.find('source', type='video/mp4')['src']
    file_name = file_name or video_url.split('/')[-1] + '.mp4'
    
    video_response = requests.get(video_source)
    with open(f'download/{file_name}', 'wb') as f:
        f.write(video_response.content)

    return f'download/{file_name}'

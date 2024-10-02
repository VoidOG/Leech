import requests
from bs4 import BeautifulSoup

def download_xhamster(video_url, file_name=None):
    """Download video from XHamster."""
    response = requests.get(video_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    video_source = soup.find('video')['src']
    file_name = file_name or video_url.split('/')[-1] + '.mp4'
    
    video_response = requests.get(video_source)
    with open(f'download/{file_name}', 'wb') as f:
        f.write(video_response.content)

    return f'download/{file_name}'

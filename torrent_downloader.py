import libtorrent as lt
import time
import os

def download_torrent(torrent_file, file_name=None):
    """Download file from a torrent."""
    ses = lt.session()
    ses.listen_on(6881, 6891)

    info = lt.torrent_info(torrent_file)
    h = ses.add_torrent({'ti': info, 'save_path': './download/'})
    
    print(f'Starting download: {torrent_file}')
    while not h.is_seed():
        s = h.status()
        print(f'Download rate: {s.download_rate / 1000} kB/s, Progress: {s.progress * 100:.2f}%')
        time.sleep(1)

    if file_name:
        os.rename(h.name(), os.path.join('./download', file_name))
        
    return os.path.join('./download', file_name or h.name())

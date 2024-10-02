import instaloader
import os

def download_instagram(link):
    try:
        # Create an instance of Instaloader
        loader = instaloader.Instaloader()

        # Extract the shortcode from the link
        shortcode = link.split("/")[-2]

        # Define the download path
        download_path = "downloads"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Download the post using the shortcode
        loader.download_post(loader.get_post(shortcode, ''))  # The second parameter is ignored for downloading

        # Get the downloaded file path
        downloaded_file = os.path.join(download_path, f"{shortcode}.jpg")  # Update based on media type if needed

        return downloaded_file  # Return the path to the downloaded file
    except Exception as e:
        return f"Error downloading Instagram media: {str(e)}"

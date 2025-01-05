import dropbox
from dropbox import Dropbox as DropboxClient
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
DOWNLOAD_FOLDER = 'downloaded_pdfs'

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_pdfs_from_dropbox(folder_path):
    """
    Downloads all PDF files from a specified Dropbox folder.

    Args:
        folder_path (str): The path to the folder in Dropbox.
    """
    dbx = DropboxClient(ACCESS_TOKEN)

    try:
        # List files in the folder
        response = dbx.files_list_folder(folder_path)
        print(response)
        return
        for entry in response.entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.pdf'):
                print(f"Downloading: {entry.name}")
                local_path = os.path.join(DOWNLOAD_FOLDER, entry.name)

                # Download the file
                with open(local_path, 'wb') as f:
                    metadata, res = dbx.files_download(entry.path_lower)
                    f.write(res.content)

                print(f"Downloaded: {entry.name} to {local_path}")

        print("All PDFs downloaded successfully.")

    except dropbox.exceptions.ApiError as e:
        print(f"Dropbox API error: {e}")

if __name__ == '__main__':
    # Specify the folder path in your Dropbox (e.g., '/my_pdfs_folder')
    DROPBOX_FOLDER_PATH = '/Gengar-1000-Research-Analysis'

    download_pdfs_from_dropbox(DROPBOX_FOLDER_PATH)

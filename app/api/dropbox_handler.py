import dropbox
from dropbox import Dropbox as DropboxClient
import os
from dotenv import load_dotenv
from consts.hidden_constants import DROPBOX_ACCESS_TOKEN

ACCESS_TOKEN = DROPBOX_ACCESS_TOKEN
DOWNLOAD_FOLDER = 'downloaded_pdfs'

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_pdfs_from_dropbox(folder_path = "", download_folder=DOWNLOAD_FOLDER, quantity=5):
    """
    Downloads all PDF files from a specified Dropbox folder.

    Args:
        folder_path (str): The path to the folder in Dropbox.
    """
    dbx = DropboxClient(ACCESS_TOKEN)

    try:
        # List files in the folder and write to file
        response = dbx.files_list_folder(folder_path)
        
        # # Write only filenames to a file
        # with open('dropbox_filenames.txt', 'w', encoding='utf-8') as f:
        #     for entry in response.entries:
        #         if isinstance(entry, dropbox.files.FileMetadata):
        #             # Write each filename on a new line
        #             f.write(f"{entry.name}\n")
                    
        # print("File names have been written to dropbox_filenames.txt")
        # return
        for entry in response.entries[:quantity]:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.pdf'):
                print(f"Downloading: {entry.name}")
                local_path = os.path.join(download_folder, entry.name)

                # Download the file
                with open(local_path, 'wb') as f:
                    metadata, res = dbx.files_download(entry.path_lower)
                    f.write(res.content)

                print(f"Downloaded: {entry.name} to {local_path}")

        print("All PDFs downloaded successfully.")
        return DOWNLOAD_FOLDER

    except dropbox.exceptions.ApiError as e:
        print(f"Dropbox API error: {e}")

def list_dropbox_folders():
    """List all folders in root directory of Dropbox"""
    dbx = DropboxClient(ACCESS_TOKEN)
    try:
        # List files/folders in root directory
        response = dbx.files_list_folder('')  # Empty string for root
        
        print("\nAvailable folders and files:")
        print("============================")
        for entry in response.entries:
            # Show if it's a folder or file
            item_type = "📁 " if isinstance(entry, dropbox.files.FolderMetadata) else "📄 "
            print(f"{item_type} {entry.path_display}")
            
            # If it's a folder, list its contents
            if isinstance(entry, dropbox.files.FolderMetadata):
                try:
                    sub_items = dbx.files_list_folder(entry.path_display)
                    for sub_entry in sub_items.entries:
                        print(f"   └── {sub_entry.name}")
                except:
                    pass
                    
    except dropbox.exceptions.ApiError as e:
        print(f"Dropbox API error: {e}")

if __name__ == '__main__':
    print("Listing all Dropbox folders...")
    # list_dropbox_folders()

    DROPBOX_FOLDER_PATH = '' # signifies the current

    download_pdfs_from_dropbox(DROPBOX_FOLDER_PATH)

import sys, os
from datetime import datetime
from azure.storage.file import FileService

def main(files):

    if not os.path.isfile('upload.config'):
        print("Settings not found. Please create an upload.config file with the Azure file share account name, access key, file share name, and folder. Each value should be on its own line.")
        exit()
    if len(files) <1:
        print("No files provided for upload. Please supply file paths as arguments.")
        exit()

    # get settings - account, key, share, and folder in subsequent lines
    with open('upload.config',"r") as config:
        settings = config.readlines()
        azure_account = settings[0].rstrip()
        azure_key = settings[1].rstrip()
        share = settings[2].rstrip()
        folder = settings[3].rstrip()

    file_service = FileService(account_name=azure_account, account_key=azure_key)

    # Arguments should just be an array of filenames.
    timestamp_suffix = datetime.now().strftime("%Y%m%d-%H%M_")
    for file in files:
        if not os.path.isfile(file):
            print(file, "not found")
        else:
            print("Uploading:", file)
            stampedfile = timestamp_suffix + os.path.basename(file)
            file_service.create_file_from_path(share, folder, stampedfile, file, progress_callback=progress)
            print(stampedfile," uploaded")

def progress(current, total):
    print(" ",current, "of", total, "uploaded")

if __name__ == "__main__":
    main(sys.argv[1:])
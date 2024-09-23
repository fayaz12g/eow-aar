import os
import requests
import zipfile
import shutil
import getpass
import hashlib

def calculate_hash(file_path):
    """Calculate the SHA256 hash of the given file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def get_remote_file_hash(url):
    """Download the file content and calculate its SHA256 hash without saving it."""
    response = requests.get(url)
    response.raise_for_status()
    sha256 = hashlib.sha256(response.content).hexdigest()
    return sha256

def download_extract_copy(input_folder, mod_name):
    username = getpass.getuser()
    directory_path = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/eow"

    zip_urls = [
        ("https://github.com/fayaz12g/aar-files/raw/main/eow/echoes.zip", "echoes.zip")
    ]

    # Check if the directory exists, create if it doesn't
    os.makedirs(directory_path, exist_ok=True)

    for zip_url, zip_filename in zip_urls:
        zip_file_source = os.path.join(directory_path, zip_filename)
        # remote_hash = get_remote_file_hash(zip_url)

        # # Check if file exists and verify its hash
        # if os.path.isfile(zip_file_source):
        #     local_hash = calculate_hash(zip_file_source)
        #     if local_hash == remote_hash:
        #         print(f"{zip_filename} is up to date.")
        #         continue
        #     else:
        #         print(f"{zip_filename} is outdated. Downloading new version.")
        # else:
        #     print(f"{zip_filename} not found. Downloading.")

        # # Download the ZIP file
        # response = requests.get(zip_url)
        # response.raise_for_status()
        # with open(zip_file_source, "wb") as file:
        #     file.write(response.content)

        # print(f"{zip_filename} downloaded and saved.")

    # Extraction and copy logic
    zip_file_source = os.path.join(directory_path, zip_filename)
    extract_folder = os.path.join(input_folder, mod_name)

    # Remove the existing destination folder if it exists
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)

    with zipfile.ZipFile(zip_file_source, "r") as zip_ref:
        zip_ref.extractall(extract_folder)
        print(f"Extracted {zip_filename} to {extract_folder}.")


    # shutil.copytree(extract_folder, romfs_folder)
    # print(f"Copied from {extract_folder} to {romfs_folder}.")



import os
import requests
import zipfile
import shutil
import getpass

def download_extract_copy(input_folder, mod_name):
    username = getpass.getuser()
    directory_path = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/eow"

    zip_urls = [
        ("https://github.com/fayaz12g/aar-files/raw/main/eow/echoes.zip", "echoes.zip")
    ]

    # Check if the directory exists, create if it doesn't
    os.makedirs(directory_path, exist_ok=True)

    # Define the final extraction folder path
    extract_folder = os.path.join(input_folder, mod_name, "romfs", "region_common", "ui")

    # Remove the existing destination folder if it exists
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)

    print(f"Checking if zip file exists.")

    # Download or extract each zip file
    for zip_url, zip_filename in zip_urls:
        zip_file_source = os.path.join(directory_path, zip_filename)
        # Check if the zip file already exists locally
        if os.path.isfile(zip_file_source):
            print(f"{zip_filename} already exists. Skipping download.")
        else:
            print(f"{zip_filename} not found. Downloading, please wait...")
            # Download the ZIP file
            response = requests.get(zip_url)
            response.raise_for_status()
            with open(zip_file_source, "wb") as file:
                file.write(response.content)
            print(f"Finished.")

        # Extract the zip file to the desired folder
        with zipfile.ZipFile(zip_file_source, "r") as zip_ref:
            zip_ref.extractall(extract_folder)
            print(f"Extracted {zip_filename} to {extract_folder}.")

    print("All zip files processed and extracted.")


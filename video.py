import subprocess
import sys
import getpass
import requests
import zipfile
import shutil
import os

def scale_video(ffmpeg_path, input_path, output_path, scaling_factor):
    # Set the scale factor
    scale_factor = float(scaling_factor)

    # Calculate the padding values
    input_width = 1920
    output_width = int(input_width * scale_factor)
    pad_left = (input_width - output_width) // 2

    # ffmpeg command to scale the video
    command = [
        ffmpeg_path,
        '-i', input_path,
        '-vf', f"scale={output_width}:1080,pad=1920:1080:{pad_left}:0,setsar=1",
        '-r', '60',  # Set the frame rate to 60fps
        '-c:a', 'copy',  # Copy the audio without re-encoding
        '-y',  # Overwrite the output file if it exists
        output_path
    ]

    # Execute the command
    subprocess.run(command, check=True)

def process_videos_in_folder(scaling_factor, output_folder):
    username = getpass.getuser()
    ffmpeg_path = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/mvdk/ffmpeg/ffmpeg.exe"
    input_folder = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/eow/movie"
    if not os.path.isdir(input_folder):
        print(f"Input folder not found: {input_folder}")
        sys.exit(1)

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".webm"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            try:
                print(f"Processing video: {filename}")
                scale_video(ffmpeg_path, input_path, output_path, scaling_factor)
                print(f"Finished video: {filename}")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while processing {filename}: {e}")

def download_video_files(input_folder):
    username = getpass.getuser()
    directory_path = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/mvdk"

    zip_urls = [
        ("https://github.com/fayaz12g/aar-files/raw/main/mvdk/Movie.zip", "Movie.zip"),
        ("https://github.com/fayaz12g/aar-files/raw/main/mvdk/ffmpeg.zip", "ffmpeg.zip"),
    ]

    # Check if the directory exists, create if it doesn't
    os.makedirs(directory_path, exist_ok=True)

    for zip_url, zip_filename in zip_urls:
        zip_folder = os.path.splitext(zip_filename)[0]
        zip_file_path = os.path.join(directory_path, zip_folder)
        zip_file_source = os.path.join(directory_path, zip_filename)

        # Check if directory exists
        if os.path.isdir(zip_file_path):
            print(f"{zip_folder} folder already exists.")
        else: 
            # Download the ZIP file
            print(f"Downloading {zip_filename}")
            response = requests.get(zip_url)
            response.raise_for_status()
            with open(zip_file_source, "wb") as file:
                file.write(response.content)
            print(f"{zip_filename} downloaded.")

            # Extract the ZIP file
            with zipfile.ZipFile(zip_file_source, "r") as zip_ref:
                zip_ref.extractall(zip_file_path)
            print(f"Extracted {zip_filename} to {zip_file_path}.")

            # Clean up the downloaded ZIP file
            os.remove(zip_file_source)
            print(f"Deleted {zip_filename} after extraction.")
    
    # Not needed as the movie scaling script will output it 

    # # Copy the extracted "Movie" folder to the "romfs" folder
    # romfs_folder = os.path.join(input_folder, "romfs")
    # video_folder_src = os.path.join(directory_path, "Movie")
    # video_folder_dst = os.path.join(romfs_folder, "Movie")

    # if os.path.exists(video_folder_src):
    #     os.makedirs(os.path.dirname(video_folder_dst), exist_ok=True)
    #     if os.path.exists(video_folder_dst):
    #         shutil.rmtree(video_folder_dst)
    #     shutil.copytree(video_folder_src, video_folder_dst)
    #     print(f"Copied Movie folder from {video_folder_src} to {video_folder_dst}.")
    # else:
    #     print(f"Source Movie folder not found at {video_folder_src}.")

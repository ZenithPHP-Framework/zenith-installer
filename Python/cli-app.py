import requests
import zipfile
import os
import shutil
from tqdm import tqdm
import time

# GitHub API URL for the latest release (replace with your actual repo's URL)
GITHUB_API_URL = "https://api.github.com/repos/ZenithPHP-Framework/full-zenith-framework/releases/latest"

def fancy_progress_bar(iterable, desc, total=None):
    return tqdm(
        iterable,
        desc=desc,
        total=total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        ncols=75,
        ascii=" ▖▘▌▝▛▜█",
        colour='cyan'
    )

def download_and_extract():
    project_name = input("Enter your project name: ")
    zip_file_path = f"{project_name}.zip"
    extract_to = project_name

    # Get the latest release download URL
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        data = response.json()
        download_url = data["zipball_url"]
    else:
        print("Error fetching latest release from GitHub.")
        return

    # Download the ZIP file with a fancy progress bar
    print("Downloading from GitHub...")
    response = requests.get(download_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(zip_file_path, 'wb') as file:
        with fancy_progress_bar(response.iter_content(chunk_size=1024), "Downloading", total_size) as bar:
            for data in bar:
                file.write(data)
                bar.update(len(data))

    # Simulate some pause for user experience
    time.sleep(1)
    
    # Extract the ZIP file to a temporary location with a fancy progress bar
    temp_extract_path = f"{project_name}_temp"
    print(f"Extracting to {temp_extract_path}...")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        with tqdm(
            zip_ref.namelist(),
            desc="Extracting",
            total=len(zip_ref.namelist()),
            unit="file",
            colour="green",
            ascii=" ▖▘▌▝▛▜█",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} files [{elapsed}]",
            ncols=75
        ) as bar:
            for file in bar:
                zip_ref.extract(file, temp_extract_path)
                bar.update(1)

    # Find the actual project folder inside the temp folder (since GitHub adds commit-hash folder)
    extracted_folder_name = os.listdir(temp_extract_path)[0]  # It will always have only one folder

    # Move contents of the extracted folder to the user-specified folder
    extracted_full_path = os.path.join(temp_extract_path, extracted_folder_name)
    print(f"Moving project files to {extract_to}...")

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    for item in os.listdir(extracted_full_path):
        shutil.move(os.path.join(extracted_full_path, item), extract_to)

    # Clean up: Remove the temporary folder and the zip file
    shutil.rmtree(temp_extract_path)
    os.remove(zip_file_path)
    
    print(f"\n✨ Project '{project_name}' created successfully!")

if __name__ == "__main__":
    download_and_extract()

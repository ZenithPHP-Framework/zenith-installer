#!/bin/bash

# Variables
GITHUB_API_URL="https://api.github.com/repos/ZenithPHP-Framework/full-zenith-framework/releases/latest"
read -p "Enter project folder name: " foldername
zipfile="/tmp/$foldername.zip"
temp_extract_path="/tmp/${foldername}_temp"

# Get the latest release download URL using curl and jq
download_url=$(curl -s "$GITHUB_API_URL" | grep zipball_url | cut -d '"' -f 4)

# Create a folder for the project
mkdir "$foldername"

# Download the zip file with a progress bar
echo "Downloading from GitHub..."
curl -L "$download_url" --progress-bar -o "$zipfile"

# Extract the zip file
echo "Extracting..."
unzip -q "$zipfile" -d "$temp_extract_path"

# Find the actual project folder (GitHub adds commit-hash folder) and move contents
extracted_folder=$(find "$temp_extract_path" -mindepth 1 -maxdepth 1 -type d)
mv "$extracted_folder"/* "$foldername"/

# Clean up
rm -rf "$temp_extract_path" "$zipfile"

echo -e "\n✨ Project '$foldername' created successfully!"

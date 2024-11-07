import os
import zipfile
import requests
import streamlit as st

def download_and_extract_instantclient():
    url = "https://www.dropbox.com/scl/fi/6dqakb7wsij6rd4gcyf7s/instantclient-basic-linux.x64-21.14.0.0.0dbru.zip?rlkey=tiedrddjkvtcxutng5vppvixq&st=sxdyp357&dl=1"
    local_filename = "instantclient-basic-linux.x64-21.14.0.0.0dbru.zip"

    # Download the file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Create the directory if it doesn't exist
    if not os.path.exists("./instantclient"):
        os.makedirs("./instantclient")

    # Unzip the file
    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            # Skip directories
            if not filename:
                continue
            # Copy file (taken from zipfile's extract)
            source = zip_ref.open(member)
            target = open(os.path.join("./instantclient", filename), "wb")
            with source, target:
                target.write(source.read())

    # Verify the contents of the directory
    extracted_files = os.listdir('./instantclient')
    st.write("Extracted files:", extracted_files)

# Call the function to download and extract the Instant Client
download_and_extract_instantclient()

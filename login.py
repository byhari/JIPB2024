import os
import zipfile
import requests
import streamlit as st

def download_and_extract_instantclient():
    url = "https://www.dropbox.com/scl/fi/tqr760sjzvs5ca09c0cvy/instantclient-basic-linux.x64-12.2.0.1.0.zip?rlkey=71h9r8gchb8iaouuqatdwg236&st=cn8v4e09&dl=1"
    local_filename = "instantclient-basic-linux.x64-12.2.0.1.0.zip"

    # Delete the existing file if it exists
    if os.path.exists(local_filename):
        os.remove(local_filename)

    # Download the file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Verify the downloaded file
    if not zipfile.is_zipfile(local_filename):
        st.error("Downloaded file is not a valid zip file.")
        return

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

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
    #if not os.path.exists("./instantclient"):
    #    os.makedirs("./instantclient")

    # Unzip the file
    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall("./instantclient")

# Call the function to download and extract the Instant Client
download_and_extract_instantclient()

# Initialize the Oracle Client
oracledb.init_oracle_client(lib_dir='./instantclient')

# Your existing code
def check_login(username, password):
    try:
        conn = oracledb.connect(user='fasdollar', password='fasdollar', dsn='172.25.1.83:1521/empdb01')
        cursor = conn.cursor()
        
        query = """
        SELECT ROLE_CODE, CH_USER_ACTIVE, CH_USER_CODE, VC_USERNAME
        FROM TAX_USERLOG_HARI
        WHERE VC_USERNAME = :username AND PASS = :password
        """
        cursor.execute(query, username=username, password=password)
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return result
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 12170:
            st.error("Connection timeout, check your connection!")
        else:
            st.error(f"An error occurred: {error.message}")
        return None

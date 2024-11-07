import os
import urllib.request
import zipfile
import streamlit as st

def download_and_extract_instantclient():
    url = "https://www.dropbox.com/scl/fi/8yxm7lqu30zkh3dr9cpxa/instantclient112.zip?rlkey=71pwxm8ng785vlrlfm30ifia4&st=drfoarfd&dl=0"
    local_filename = "instantclient112.zip"

    # Download the file
    urllib.request.urlretrieve(url, local_filename)

    # Check if the file is downloaded correctly
    if os.path.getsize(local_filename) < 100:  # Adjust the size check as needed
        st.error("Downloaded file is too small, possibly an error page.")
        return

    # Unzip the file
    try:
        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            zip_ref.extractall("./main")
    except zipfile.BadZipFile:
        st.error("The downloaded file is not a valid ZIP file.")

# Call the function to download and extract the Instant Client
download_and_extract_instantclient()

# Initialize the Oracle Client
oracledb.init_oracle_client(lib_dir='./main')

# Your existing database connection and login logic
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

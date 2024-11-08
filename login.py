import os
import zipfile
import requests
import streamlit as st
import oracledb
import ctypes

def check_libaio():
    try:
        # Attempt to load the libaio library
        libaio = ctypes.CDLL('libaio.so.1')
        st.write("libaio is installed and accessible.")
    except OSError as e:
        st.error(f"libaio is not accessible: {e}")

# Call the function to check libaio
check_libaio()


def download_and_extract_instantclient():
    url = "https://www.dropbox.com/scl/fi/3to8vnel6xuuq32wf6nuw/instantclient_12_2.zip?rlkey=v4clodbdr69igevmnrastr3kj&st=yo8xvxnr&dl=1"
    local_filename = "instantclient_12_2.zip"

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

# Set environment variable
os.environ['LD_LIBRARY_PATH'] = os.path.abspath('./instantclient')

# Verify environment variable
st.write("LD_LIBRARY_PATH:", os.environ.get('LD_LIBRARY_PATH'))

# Check file permissions
st.write("Permissions for instantclient:", os.access('./instantclient/libclntsh.so', os.R_OK))

# Initialize the Oracle Client
oracledb.init_oracle_client(lib_dir=os.path.abspath('./instantclient'))

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

# Example usage of the check_login function
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    result = check_login(username, password)
    if result:
        st.success("Login successful!")
    else:
        st.error("Login failed!")

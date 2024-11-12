import os
import zipfile
import requests
import streamlit as st
import oracledb
import ctypes

def check_libaio():
    try:
        libaio = ctypes.CDLL('libaio.so.1')
        st.write("libaio is installed and accessible.")
    except OSError as e:
        st.error(f"libaio is not accessible: {e}")

check_libaio()

def download_and_extract_instantclient():
    url = "https://drive.google.com/uc?export=download&id=1DUE_RRp9UVkwiL0mhqrgP8eNmCaCLJ7O"
    local_filename = "instantclient-basic-linux.x64-23.zip"

    if os.path.exists(local_filename):
        os.remove(local_filename)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    if not zipfile.is_zipfile(local_filename):
        st.error("Downloaded file is not a valid zip file.")
        return

    if not os.path.exists("./instantclient"):
        os.makedirs("./instantclient")

    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall("./instantclient")

    extracted_files = os.listdir('./instantclient')
    st.write("Extracted files:", extracted_files)

download_and_extract_instantclient()

os.environ['LD_LIBRARY_PATH'] = os.path.abspath('./instantclient')
st.write("LD_LIBRARY_PATH:", os.environ.get('LD_LIBRARY_PATH'))

# Set correct permissions
for root, dirs, files in os.walk('./instantclient'):
    for file in files:
        os.chmod(os.path.join(root, file), 0o755)

st.write("Permissions for instantclient:", os.access('./instantclient/libclntsh.so', os.R_OK))

oracledb.init_oracle_client(lib_dir=os.path.abspath('./instantclient'))

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

username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    result = check_login(username, password)
    if result:
        st.success("Login successful!")
    else:
        st.error("Login failed!")

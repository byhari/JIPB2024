import os
import urllib.request
import zipfile
import streamlit as st
import oracledb

def download_and_extract_instantclient():
    url = "https://www.dropbox.com/scl/fi/1s7me50wgi14tso9zmjrz/instantclient_12_1.zip?rlkey=8rmbxrshjn6r44j898c1hiai1&st=sdslt96n&dl=1"
    local_filename = "instantclient_12_1.zip"

    # Download the file
    st.write("Downloading Oracle Instant Client...")
    urllib.request.urlretrieve(url, local_filename)

    # Check if the file is downloaded correctly
    if os.path.getsize(local_filename) < 100:  # Adjust the size check as needed
        st.error("Downloaded file is too small, possibly an error page.")
        return

    # Unzip the file
    try:
        st.write("Extracting Oracle Instant Client...")
        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            zip_ref.extractall("./instantclient")
    except zipfile.BadZipFile:
        st.error("The downloaded file is not a valid ZIP file.")
        return

# Call the function to download and extract the Instant Client
download_and_extract_instantclient()

# Initialize the Oracle Client
try:
    oracledb.init_oracle_client(lib_dir='./instantclient')
except oracledb.DatabaseError as e:
    st.error(f"Failed to initialize Oracle Client: {e}")
    st.stop()

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

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# Function to handle exit
def handle_exit():
    st.session_state.clear()
    st.session_state['page'] = 'login'

# Login Page
if st.session_state['page'] == 'login':
    st.title('Login Page')

    username = st.text_input('Username', key='username').upper()
    password = st.text_input('Password', type='password', key='password').upper()

    if st.button('OK', key='login_ok_button'):
        if not username or not password:
            st.error('Please login first!')
        else:
            result = check_login(username, password)
            if result is None:
                st.error('Login failed, user name or password not match')
            else:
                role_code, user_active, user_code, vc_username = result
                if user_active == 'N':
                    st.error('Login failed, user is not active')
                else:
                    st.success('Login success')
                    st.session_state['user_code'] = user_code
                    st.session_state['vc_username'] = vc_username
                    st.session_state['page'] = 'jipb'

if st.button('EXIT', key='exit_button'):
    handle_exit()

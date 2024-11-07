from sqlalchemy import create_engine
import oracledb
import streamlit as st
import cx_Oracle
import pyodbc
import pandas as pd
from datetime import datetime
import os

parts = ["oraociei11.dll.part1", "oraociei11.dll.part2", "oraociei11.dll.part3", "oraociei11.dll.part4", "oraociei11.dll.part5", "oraociei11.dll.part6", "oraociei11.dll.part7"]  # Add all parts here
with open("largefile.zip", "wb") as outfile:
    for part in parts:
        with open(part, "rb") as infile:
            outfile.write(infile.read())

# Unzip the file if necessary
import zipfile
with zipfile.ZipFile("largefile.zip", 'r') as zip_ref:
    zip_ref.extractall("./main")



# Function to check login credentials
def check_login(username, password):
    try:
        # Initialize the Oracle Client
        oracledb.init_oracle_client(lib_dir=r"./main")  # Adjust the path as needed
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

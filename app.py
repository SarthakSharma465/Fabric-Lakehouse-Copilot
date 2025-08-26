import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI


# Load environment variables from .env (optional)
load_dotenv()

# Environment Variables
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_KEY = os.getenv("API_KEY")
TENANT_ID = os.getenv("TENANT_ID")
API_KEY = os.getenv("API_KEY")

# Build connection string
conn = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={SERVER};"
    f"Database={DATABASE};"
    "Authentication=ActiveDirectoryServicePrincipal;"
    f"UID={CLIENT_ID};"
    f"PWD={CLIENT_SECRET};"
    f"Authority Id={TENANT_ID};"
    "Encrypt=yes;TrustServerCertificate=no;"
)

def TestConnection(conn_str):
    """Test the database connection by running a simple query."""
    try:
        with pyodbc.connect(conn_str, timeout=30) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 AS test_value;")
            response = cursor.fetchone()  # Get one row
            return f"Connection Successful! Test Value = {response.test_value}"
    except Exception as e:
        return f"Connection Failed! Error: {e}"
    
def api_call(system, user):
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # or "gpt-4o", "gpt-3.5-turbo", etc.
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return response.choices[0].message.content.strip()


# --- Streamlit UI ---
print(TestConnection(conn_str=conn))

st.set_page_config(layout="wide")
st.title("AI Interaction Layer")

if st.button("SQL Connection", key="1"):
    st.text(TestConnection(conn_str=conn))

user_prompt = st.text_area("Enter your prompt:")
system_prompt = "You are a helpful assistant"

if st.button("Ask AI", key="2"):
    ai_response = api_call(system=system_prompt, user=user_prompt)
    st.text(ai_response)







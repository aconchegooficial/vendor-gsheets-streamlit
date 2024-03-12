import streamlit as st
from streamlit_gsheets import GSheetsConnection


def connection():
    # ESTABLISHING A GOOGLE SHEETS CONNECTION
    conn = st.connection("gsheets", type=GSheetsConnection)

    # FETCH EXISTING DATA
    existing_data = conn.read(worksheet="VENDAS", usecols=list(range(12)), ttl=5)
    existing_data = existing_data.dropna(how="all")

    return conn, existing_data
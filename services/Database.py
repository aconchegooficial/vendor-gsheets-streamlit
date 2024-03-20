import streamlit as st
from streamlit_gsheets import GSheetsConnection


class Database:
    def __init__(self, worksheets: list = []):
        
        self.conn = st.connection("gsheets", type=GSheetsConnection)
        self.worksheets = {}

        for info in worksheets:
            self._conn(info[0], info[1])

    
    def _conn(self, worksheet_name, cols):
        self.worksheets[worksheet_name] = self.conn.read(worksheet=worksheet_name, usecols=list(range(cols)), ttl=5)
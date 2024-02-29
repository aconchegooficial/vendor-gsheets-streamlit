import streamlit as st

class Style:
    def __init__(self, style_path):
        self.style_path = style_path

    def connect_stylesheet(self):
        with open(self.style_path) as f:
            st.markdown(f"<style>{f.read()}</style>",
                unsafe_allow_html=True)
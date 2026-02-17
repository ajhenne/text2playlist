import base64
import streamlit as st


def get_svg_html(path):
    
    with open(path, "rb") as f:
        base64_svg = base64.b64encode(f.read()).decode("utf-8")
        
    return f'<img src="data:image/svg+xml;base64,{base64_svg}" width="25">'
import streamlit as st

from modes.text2playlist import page_text2playlist
from modes.permalink import page_permalink
from modes.privacy import page_privacy

from functions.css import (custom_css,
                           footer_css,
                           dialog_css)

st.set_page_config(page_title="text2playlist")


if "processed_data" not in st.session_state:
    st.session_state.processed_data = None
        
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(dialog_css, unsafe_allow_html=True)
# st.markdown(footer_css, unsafe_allow_html=True)


if "p" in st.query_params:
    page_permalink(st.query_params['p'])

elif st.query_params.get('v') == 'privacy':
    page_privacy()
    
else:
    page_text2playlist()




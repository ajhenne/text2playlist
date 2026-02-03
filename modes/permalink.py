import streamlit as st

from functions.general import link_from_permalink

def page_permalink(playlist_id):

    playlist_url = link_from_permalink(playlist_id)
    print(playlist_url)


    if playlist_url:
        st.button('YouTube')

    else:
        st.error(":red[**ERROR**:] Permalink not found or has expired")
        
    return
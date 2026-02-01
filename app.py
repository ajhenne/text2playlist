import streamlit as st
from functions import extract_urls, get_titles, generate_playlist_link
from functions import custom_css, footer_css

st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(footer_css, unsafe_allow_html=True)

st.title("chat2playlist")

st.text("Extract all music links from a text file (e.g. WhatsApp group chat) into a YouTube playlist.")

uploaded_file = st.file_uploader("", type='txt', label_visibility="collapsed")

if uploaded_file:

    with st.spinner("Getting your playlist...", width='stretch'):
        content = uploaded_file.read().decode('utf-8')
        yt_links, other_links = extract_urls(content)

        playlist_link = generate_playlist_link(yt_links)

        all_links = yt_links
        all_titles = get_titles(all_links)
        
    if len(all_links) > 50:
        # TODO
        st.info("There is a 50 song limit to created playlists, enforced by YouTube. Your playlist will be split into several links.")

    with st.container(border=True):

        st.link_button("YouTube Playlist", playlist_link, width='stretch', type='primary')

        for title, link in zip(all_titles, all_links):
            st.markdown(f":small[[{title}]({link})]")
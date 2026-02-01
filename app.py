import streamlit as st

from functions import extract_urls, generate_playlist_link

st.title("Playlist Creator")

st.text("Take txt files (for example, WhatsApp chat logs), search for all music links and output a YouTube playlist.")

uploaded_file = st.file_uploader("Uploaded .txt file", type='txt')

if uploaded_file:

    content = uploaded_file.read().decode('utf-8')
    yt_links, other_links = extract_urls(content)

    # ignore other_links for now
    all_links = yt_links

    playlist_link = generate_playlist_link(yt_links)
    st.success("Success!")
    st.video(yt_links[0])
    st.text(yt_links[0])
    st.link_button("Open YouTube playlist", playlist_link)
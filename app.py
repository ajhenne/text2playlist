import streamlit as st
from functions import extract_urls, convert_to_youtube, generate_playlist_link
from functions import custom_css, footer_css

st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(footer_css, unsafe_allow_html=True)

st.title(":primary[chat2playlist]")

st.text("Extract music into a YouTube playlist. Designed for messaging service chat logs, but works for any text file that includes links.")

uploaded_file = st.file_uploader("", type='txt', label_visibility="collapsed")

if uploaded_file:

    with st.spinner("Getting your playlist...", width='stretch'):
        content = uploaded_file.read().decode('utf-8')

        yt_links, other_links = extract_urls(content)
        all_links = yt_links + convert_to_youtube(other_links)

        playlist_link = generate_playlist_link(all_links)


    with st.container(border=False):

        if not len(all_links):
            st.markdown(":red[**ERROR:**] No music could be found in this file. If you think this is incorrect, please submit an issue on the [GitHub](https://github.com/ajhenne/chat2playlist).")
            
        elif len(all_links) > 50:
            # TODO
            st.info("There is a 50 song limit to created playlists, enforced by YouTube. Your playlist will be split into several links.")

        else:

            st.markdown(f"**:green[SUCCESS:]** found {len(all_links)} songs from {len(yt_links)+len(other_links)} links")
            st.link_button("YouTube Playlist", playlist_link, width='stretch', type='primary')
            
            col_clipboard, col_permalink = st.columns([0.25, 0.25], vertical_alignment='center')

            with col_clipboard:
                st.button("Copy to clipboard", use_container_width=True)

            with col_permalink:
                st.button("Save permalink", use_container_width=True)

else:
    pass
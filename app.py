import streamlit as st

from functions import extract_urls, convert_to_youtube, generate_playlist_link
from functions import custom_css, footer_css

if "processed_data" not in st.session_state:
    st.session_state.processed_data = None

st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(footer_css, unsafe_allow_html=True)

st.title(":primary[chat2playlist]")

st.text("Extract music into a YouTube playlist. Designed for messaging service chat logs, but works for any text file that includes links.")


uploaded_file = st.file_uploader("upload_file", type='txt', label_visibility="collapsed")

if uploaded_file:

    file_id = uploaded_file.name + str(uploaded_file.size)

    if st.session_state.processed_data is None or st.session_state.processed_data['id'] != file_id:

        with st.spinner("Getting your playlist...", width='stretch'):
            content = uploaded_file.read().decode('utf-8')
            yt_links, other_links = extract_urls(content)
            all_links = yt_links + convert_to_youtube(other_links)
            playlist_link = generate_playlist_link(all_links)

            st.session_state.processed_data = {
                'id': file_id, 'all_links': all_links,
                'yt_count': len(yt_links), 'other_count': len(other_links),
                'playlist_link': playlist_link
            }

    data = st.session_state.processed_data

    if not len(data['all_links']):
        st.markdown(":red[**ERROR:**] No music could be found in this file. If you think this is incorrect, \
                    please submit an issue on the [GitHub](https://github.com/ajhenne/chat2playlist).")
    
    else:
        
        if len(data['all_links']) > 50:
            # TODO - split into multiple playlists?
            st.info("There is a 50 song limit to created playlists, enforced by YouTube. Your playlist will only include \
                    the first 50.")

        st.markdown(f"**:green[SUCCESS:]** found {len(data['all_links'])} songs from {data['yt_count']+data['other_count']} links")
        st.link_button("YouTube Playlist", data['playlist_link'], width='stretch', type='primary')
        
        col_clipboard, col_permalink = st.columns([0.5, 0.5], vertical_alignment='center')

        with col_clipboard:
            st.button("Copy to clipboard", use_container_width=True)

        with col_permalink:
            st.button("Save permalink", use_container_width=True)

else:
    pass
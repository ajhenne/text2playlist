import streamlit as st
import secrets
import string
from functions.general import get_link_list, url_checker, resolve_tracks, generate_youtube_link, display_spotify_list
from functions.general import save_permalink, make_table_links

from functions.general import get_icons_html

ICONS = get_icons_html()


def page_text2playlist():

    st.title(":primary[text2playlist]")

    st.text("Extract music links from a large textfile. Can be output directly into a YouTube playlist, as a list to import into Spotify, or as a list of song and artist names.")

    uploaded_file = st.file_uploader("upload_file", type='txt', label_visibility="collapsed")
    
    if uploaded_file:

        file_id = uploaded_file.name + str(uploaded_file.size)

        if st.session_state.processed_data is None or st.session_state.processed_data['id'] != file_id:
        # if True:

            with st.spinner("Getting track details. This may take up to a minute...", width='stretch'):

                content = uploaded_file.read().decode('utf-8')
                raw_links = get_link_list(content)
                link_list = [url for url in raw_links if url_checker(url)]
                data = resolve_tracks(link_list)

                st.session_state.processed_data = {
                    'id': file_id,
                    'song_data': data,
                    'song_count': len(data),
                    'raw_count': len(raw_links),
                }
                
        data = st.session_state.processed_data
        song_data = data['song_data']
        
        if not len(song_data):
            st.markdown(":red[**ERROR:**] No valid music links could be found in this file.")
            st.markdown("The links may be playlist or album links, which are not currently supported, \
                rather than indvidual links. Or, the music service may not be currently supported. If \
                you would like a music service supported, or you think an error has occurred, please  \
                submit an issue on the [GitHub](https://github.com/ajhenne/chat2playlist).")
            return
        
        youtube_link = generate_youtube_link(song_data['link_youtube'])
        
        st.link_button("YouTube", youtube_link, width='stretch')
        if st.button("Spotify", '1', width='stretch'):
            display_spotify_list(song_data['link_spotify'])
        
        # col_clipboard, col_permalink = st.columns([0.5, 0.5], vertical_alignment='center')
        # with col_clipboard:
        #     st.button("Copy to clipboard", use_container_width=True)
        # with col_permalink:
        #     if st.button("Save permalink", use_container_width=True):
        #         code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

        #         if save_permalink(code, data['playlist_link']):
        #             final_url = f"https://chat2playlist.streamlit.app/?p={code}"
        #             st.success("Permalink created")
        #             st.code(final_url, language=None)
        #         else:
        #             st.error("error")

        st.subheader(":primary[Tracklist]")
        
        for row in song_data.itertuples():
            col_title, col_artist, col_link = st.columns([0.55, 0.35, 0.1])
            with col_title:
                st.write(row.raw_data)
                
                # TODO troubleshooting a failed url with no odesli details. need to filter out somewhere
                # tried to re-add rawurl column need to test why apdnas says no rawdata column. likely just filtered out or somethin somehwre?
            with col_artist:
                st.write(row.artist)
            with col_link:
                st.markdown(f"{make_table_links(row.link_youtube, row.link_spotify, ICONS)}", unsafe_allow_html=True)     
                
                
        # output_format = st.selectbox("Select output", options=["YouTube", "Spotify"], width=300)

        # if not len(data['all_links']):
        #     st.markdown(":red[**ERROR:**] No music could be found in this file. If you think this is incorrect, \
        #                 please submit an issue on the [GitHub](https://github.com/ajhenne/chat2playlist).")
        
        # else:

        #     if len(data['all_links']) > 50:
        #         # TODO - split into multiple playlists?
        #         st.info("There is a 50 song limit to created playlists, enforced by YouTube. Your playlist will only include \
        #                 the first 50.")

        #     st.markdown(f"**:green[SUCCESS:]** found {len(data['all_links'])} songs from {data['yt_count']+data['other_count']} links")
        #     st.link_button("YouTube Playlist", data['playlist_link'], width='stretch', type='primary')
            
        #     col_clipboard, col_permalink = st.columns([0.5, 0.5], vertical_alignment='center')

        #     with col_clipboard:
        #         st.button("Copy to clipboard", use_container_width=True)

        #     with col_permalink:

        #         if st.button("Save permalink", use_container_width=True):
        #             code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

        #             if save_permalink(code, data['playlist_link']):
        #                 final_url = f"https://chat2playlist.streamlit.app/?p={code}"
        #                 st.success("Permalink created")
        #                 st.code(final_url, language=None)
        #             else:
        #                 st.error("error")
    else:
        pass


        return
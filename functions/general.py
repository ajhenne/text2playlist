import re
import requests
import pandas as pd
import streamlit as st

from streamlit_gsheets import GSheetsConnection

def extract_urls(text):
    """Get URLs from a block of text."""

    url_pattern = r'(https?://[^\s]+)'
    links = re.findall(url_pattern, text)

    yt_links = [url for url in links if ("youtube.com/watch" in url) or ("youtu.be" in url)]
    other_links = [url for url in links if url not in yt_links]
    
    return yt_links, other_links

@st.cache_data
def odesli_search(url):
    """Find YT link using Odesli API."""
    try:
        response = requests.get(f"https://api.song.link/v1-alpha.1/links?url={url}")
        
        if response.status_code == 200:
            data = response.json()
            yt_data = data.get('linksByPlatform', {}).get('youtube')

            if yt_data:
                return yt_data.get('url')
    except:
        return 
    

def url_checker(url):
    """Try to avoid links that aren't a specific song."""
    u = url.lower()

    # quick guard clase - need to manually verify links to add more services
    music_services = ["youtube.com", "youtu.be", "spotify.com", "soundcloud.com", "music.apple.com"]
    if not any(service in u for service in music_services):
        return False

    if "youtube.com/playlist" in u:
        return False
    
    if "music.apple.com" in u and ("album" in u and "?i=" not in u): #album ok if it points to track
        return False 
    
    if "spotify.com" in u and "track" not in u:
        return False
    
    if "soundcloud.com" in u and ("sets" in u and "?in=" not in u): # sets(album) ok if it points to track
        return False

    return True
    
    
@st.cache_data
def convert_to_youtube(link_list):
    """Converts links from other sources into a YouTube link."""
            
    youtube_links = []

    for url in link_list:
        if url_checker(url):
            youtube_url = odesli_search(url)
            if youtube_url is not None:
                youtube_links.append(youtube_url)

    return youtube_links


def generate_playlist_link(link_list):
    """Convert a list of links into a YouTube temporary playlist link."""
    video_ids = []

    for url in link_list:

        if "v=" in url:
            video_ids.append(url.split("v=")[1].split("&")[0])
        elif "youtu.be/" in url:
            video_ids.append(url.split("youtu.be/")[1].split("?")[0])

    return f"https://www.youtube.com/watch_videos?video_ids={','.join(video_ids)}"


###############################################################################

def save_permalink(permalink, yt_link):
    conn = st.connection('gsheets', type=GSheetsConnection)
    df = conn.read(ttl=0)

    if permalink in df['permalink'].values:
        return False
    
    new_row = pd.DataFrame([{"permalink": permalink, "yt_link": yt_link}])
    updated_df = pd.concat([df, new_row], ignore_index=True)

    conn.update(data=updated_df)
    return True


def link_from_permalink(permalink):
    conn = st.connection('gsheets', type=GSheetsConnection)
    df = conn.read(ttl="10m")

    match = df[df['permalink'] == permalink]

    if match.empty:
        return None
    
    return match.iloc[0]['yt_link']


###############################################################################

custom_css = """
<style>
.stMainBlockContainer{
    padding-top: 50px;
}

.st-emotion-cache-198znwi hr {
    margin-top: -5px;
    margin-bottom: 25px;
    }
</style>
"""

footer_css = """
<style>


.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px 0;
    z-index: 999;
    
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 40px;
}

.footer a {
    color: rgb(153, 153, 153);
    text-decoration: none;
    display: flex;
    align-items: center;

}

.footer a:hover {
    text-decoration: underline;
    color: rgb(255, 197, 138);
}

</style>

<div class="footer">
    <a href="https://github.com/ajhenne/chat2playlist" target="_blank">GitHub</a>
    <a href="https://www.linkedin.com/in/ajhennessy/" target="_blank">LinkedIn</a>
    <a href="./?v=privacy" target="_blank">Privacy Statement</a>
</div>
"""

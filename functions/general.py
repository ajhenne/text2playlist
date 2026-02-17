import re
import requests
import pandas as pd
import streamlit as st
import base64

from concurrent.futures import ThreadPoolExecutor

from streamlit_gsheets import GSheetsConnection

###############################################################################
### ICONS

def get_icons_html():
    """Get HTML from svgs for coloured and greyed icons."""
    
    output_html = []
    
    for svc in ('youtube', 'spotify', 'soundcloud'):
        with open(f'assets/{svc}.svg', 'rb') as f:
            base64_svg = base64.b64encode(f.read()).decode("utf-8")
            coloured = f'<img src="data:image/svg+xml;base64,{base64_svg}" width="25">'
            
        with open(f'assets/{svc}_grey.svg', 'rb') as f:
            base64_svg = base64.b64encode(f.read()).decode("utf-8")
            grey = f'<img src="data:image/svg+xml;base64,{base64_svg}" width="25">'
        
        output_html.append([coloured, grey])
        
    return output_html


def make_table_links(link_youtube, link_spotify, icons):
    """Create table row of links for a song."""
    
    icon_youtube, icon_spotify, _ = icons
     
    if link_youtube:
        output_youtube = f'<a href="{link_youtube}" target="_blank">{icon_youtube[0]}</a>'
    else:
        output_youtube = icon_youtube[1]
        
    if link_spotify:
        output_spotify = f'<a href="{link_spotify}" target="_blank">{icon_spotify[0]}</a>'
    else:
        output_spotify = icon_spotify[1]
        
    return f'{output_youtube}&nbsp;{output_spotify}'
    

###############################################################################
### LINK PROCESSING

def get_link_list(text):
    """Get URLs from text and output in specified format."""

    url_pattern = r'(https?://[^\s]+)'
    link_list = re.findall(url_pattern, text)    

    return link_list


def url_checker(url):
    """Filter out links from unknown services, or those that aren't song links."""
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


# @st.cache_data
def resolve_tracks(link_list):
    """Get a dataframe of results for all inputted links."""

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(odesli_search, link_list))
        
    valid_results = [r for r in results if r is not None]

    return pd.DataFrame(valid_results)


# @st.cache_data
def odesli_search(url):
    """Find metadata using Odesli API."""

    try:
        response = requests.get(f"https://api.song.link/v1-alpha.1/links?url={url}")
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        entities = data.get('entitiesByUniqueId', {})
        links = data.get('linksByPlatform', {})
        
        title = None
        artist = None
        
        spotify_key = next((k for k in entities if k.startswith("SPOTIFY_SONG")), None)
        soundcloud_key = next((k for k in entities if k.startswith("SOUNDCLOUD_SONG")), None)
        youtube_key = next((k for k in entities if k.startswith("YOUTUBE_VIDEO")), None)
                
        # prefer spotify -> soundcloud -> youtube for name & artist metadata
        for key in [spotify_key, soundcloud_key, youtube_key]:
            if key and not title:
                title = entities[key].get('title')
            if key and not artist:
                artist = entities[key].get('artistName')
                
        link_youtube = links.get('youtube', {}).get('url')
        link_spotify = links.get('spotify', {}).get('url')
        # youtubeMusic, soundcloud
        
        return {'title': title, 'artist': artist,
                'link_youtube': link_youtube,
                'link_spotify': link_spotify,
                'raw_link': url}
    
    except: 
        return 
    

###############################################################################

# @st.cache_data
def generate_youtube_link(link_list):
    """Convert a list of links into a YouTube temporary playlist link."""
    video_ids = []
    
    link_list = [x for x in link_list if x is not None]
    
    for url in link_list:

        if "v=" in url:
            video_ids.append(url.split("v=")[1].split("&")[0])
        elif "youtu.be/" in url:
            video_ids.append(url.split("youtu.be/")[1].split("?")[0])

    return f"https://www.youtube.com/watch_videos?video_ids={','.join(video_ids)}"


@st.dialog(":primary[Spotify]", width="medium")
def display_spotify_list(link_list):
    
    st.text("Copy this list and open the Spotify Desktop app or Spotify Web. Make a new playlist, or go to an existing playlist, and click paste (Ctrl+V or Cmd+V) to paste the tracks int othe playlist.")
    display_list = "\n".join(link_list.dropna().astype(str))
    st.code(display_list, language=None, width='stretch', height=300)
    
    return





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
import re

def extract_urls(text):

    url_pattern = r'(https?://[^\s]+)'
    links = re.findall(url_pattern, text)

    yt_links = [url for url in links if ("youtube.com/watch" in url) or ("youtu.be" in url)]
    other_links = [url for url in links if url not in yt_links]
    
    return yt_links, other_links


def generate_playlist_link(link_list):

    video_ids = []

    for url in link_list:

        if "v=" in url:
            video_ids.append(url.split("v=")[1].split("&")[0])
        elif "youtu.be/" in url:
            video_ids.append(url.split("youtu.be/")[1].split("?")[0])

    return f"https://www.youtube.com/watch_videos?video_ids={','.join(video_ids)}"
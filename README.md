# text2playlist

[text2playlist.streamlit.app](https://text2playlist.streamlit.app)

A tool to convert music links within text files into a playlist. Designed specifically for converting all the music shared in a messaging chat log (e.g. music sharing group chats), but in principle works for any text file.

## Features 
- Simple regex to find all links from an inputted `.txt` file.
- Supports direct YouTube or YouTube music links, or uses [Odesli](https://odesli.co) to search for the equivalent YouTube link, currently supporting:
    - Spotify
    - SoundCloud
    - Apple Music
- Several output formats, currently supporting:
    - List of song names, artists and individual links
    - YouTube playlist link
    - Spotify URL list for directly pasting into playlists
- No API or account linking required.
- Web interface for easy file upload.

## Support

**Other music services:** I'm happy to support other music services, it just requires me checking the URLs - please raise a GitHub issue.

**Text file not working:** This should work for any text file, but there may be specific quirks that cause failure. Raise a GitHub issue and I can account for this.

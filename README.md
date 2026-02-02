# chat2playlist

[chat2playlist.streamlit.app](https://chat2playlist.streamlit.app)

A tool to convert music links within text files into a playable YouTube playlist. Designed specifically for converting all the music shared in a messaging chat log (e.g. music sharing group chats), but in principle works for any text file.

## Features 
- Simple regex to find all links from an inputted `.txt` file.
- Supports direct YouTube or YouTube music links, or uses [Odesli](https://odesli.co) to search for the equivalent YouTube link, currently supporting:
    - Spotify
    - SoundCloud
    - Apple Music
- Instant generation of a URL that contains all the music into a playable queue - no API or account linking required.
- Web interface for easy file upload.
- (*planned*) Create a nicer looking shortened permalink.

## Support

**Other music services:** I'm happy to support other music services, it just requires me checking the URLs - raise a GitHub issue.

**Text file not working:** This should work for any text file, but there may be specific quirks that cause failure. Raise a GitHub issue and I can account for this.

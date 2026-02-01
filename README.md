# chat2playlist

A tool to convert music links within txt files into a playable YouTube playlist. Great for converting chat logs from groups in WhatsApp instantly into a shareable link.

- Simple regex to find all links from an inputted `.txt` file.
- Supports direct YouTube or YouTube music links, (*planned*) or searches YouTube for the best match from other links (e.g. Spotify, SoundCloud).
- Instant generation of a URL that contains all the music into a playable queue - no API or account linking required.
- Web interface for easy file upload.
- (*planned*) Create a nicer looking shortened permalink.

## Officially Supports

Chat log source:
- WhatsApp

Supports links from:
- YouTube or YouTube Music

In principle these are the specific cases that are directly supported, butthis should work for the exported logs from any similar messaging service, or more generally any txt file. If you encounter any quirks from other sources, please create a GitHub issue and I can account for this.

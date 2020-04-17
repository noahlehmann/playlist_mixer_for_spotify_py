# Playlist Mixer for Spotify

## Setup
create credentials.py for import

### credentials.py
````python
USERNAME = 'username'  # login username for spotify account
CLIENT_ID = 'client_id'  # from dev console in spotify
CLIENT_SECRET = 'secret'  # from dev console in spotify
REDIRECT_URL = 'redirect_url'  # manually defined in spotify console
````

## Usage
call

````shell script
python playlist_mixer [username] [playlist]
````
Where:
- username = username of users tracks to merge with
- playlist (optional) = name of playlist to be created, defaults to "{owner}_{username}"


First usage after 1h will prompt for auth in standard browser. 
After that tokens will be automatically renewed by the spotipy package in between the 1h interval.
Cached tokens for users will be saved in .cache-\[username] files
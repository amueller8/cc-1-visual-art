"""
Abby Mueller
"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


#set environment variables https://phoenixnap.com/kb/set-environment-variable-mac

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = sp.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])


#playlist iteration from https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py 
pl_id = 'spotify:playlist:1umwX5x9YfdOYZDWR5BjUO'
offset = 0

while True:
    response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,items.track.name,total',
                                 additional_types=['track'])
    
    if len(response['items']) == 0:
        break
    
    print(response['items'])
    offset = offset + len(response['items'])
    print(offset, "/", response['total'])

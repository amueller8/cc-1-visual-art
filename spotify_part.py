"""
Abby Mueller
"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


#set environment variables https://phoenixnap.com/kb/set-environment-variable-mac

def get_playlist_id():
    print("What is the id of the playlist?")
    play_id_num = input()
    return 'spotify:playlist:' + str(play_id_num)

def get_playlist_track_info(sp, uri):
    """
    Get playlist track info and aggregate into dataframes.
    Args:
    sp, spotipy credentials object
    uri, resource id for playlist
    
    """
    track_uri = []
    track_name = []
    track_artist = []


    offset = 0 #tracks how many items in the playlist we look at
    response = sp.playlist_items(uri,
                                offset=offset,
                                fields='items.track.id,items.track.name,items.track.artists, total',
                                additional_types=['track'])

    if len(response['items']) == 0:
        print("Invalid playlist- no songs")
    else:
        
        for item in response['items']:
            #print(item)
            artists = item["track"]["artists"]
            track_id = item["track"]["id"]
            track_n = item["track"]["name"]
        
            track_uri.append(track_id)
            track_name.append(track_n)

            artist_name = artists[0]["name"]
        
            if len(artists) > 1:
                artist2_name = artists[1]["name"]
                

                track_artist.append([artist_name, artist2_name])
            else:
                track_artist.append([artist_name])
            
        print(track_uri, track_name, track_artist)

        #print(response['items.track'])
        offset = offset + len(response['items'])
        print(offset, "/", response['total'])


#1umwX5x9YfdOYZDWR5BjUO
#playlist iteration from https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py 
#pl_id = 'spotify:playlist:' + str(play_id_num)
#print(pl_id)


#while True:



def main():

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    print("x")
    id = get_playlist_id()
    get_playlist_track_info(sp, id)

if __name__ == "__main__":
    main()
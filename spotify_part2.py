"""
Abby Mueller
"""
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup as bs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import math


#set environment variables https://phoenixnap.com/kb/set-environment-variable-mac
class SongMarkov:
    def __init__(self, transition_matrix):
        self.transition_matrix = transition_matrix
        self.indices = list(transition_matrix.keys())
    
    def get_next_song(self, curr_song):
        return np.random.choice(
            self.indices, 
            p=[self.transition_matrix[curr_song][next_index] for next_index in self.indices]
        )
    
    def create_transitions(self, current_song, len_param=4):
        songs = []
        while len(songs) < len_param:
            next_song= self.get_next_song(current_song)
            songs.append(next_song) #don't need to set melody equal to this
        
        #print("THe songs!!")
        return songs

    

        #markov chain of probabilities of 

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
        df1 = pd.DataFrame(response)

        for i, x in df1['items'].items():
        
            artists = x["track"]['artists']

            track_uri.append(x["track"]['id'])
            track_name.append(x["track"]['name'])
            artist_name = artists[0]["name"]
        
            if len(artists) > 1:
                artist2_name = artists[1]["name"]
                

                track_artist.append([artist_name, artist2_name])
            else:
                track_artist.append([artist_name])

        df2 = pd.DataFrame({
            'id':track_uri,
            'name': track_name,
            'artist': track_artist
        })

        #print(df2)

        #print(response['items.track'])
        offset = offset + len(response['items'])
        #print(offset, "/", response['total'])

        return df2, offset

def create_matrix(df):
    #get lengths of each song title, total up
    total_length = 0
    for song in df["name"]:
        print(len(song))
        total_length += len(song)
    
    print(total_length)
    print(len(df["name"]))

    differences = {}
    shape = df["name"]
    #now, for total length:
    print("vals",len(df["name"]))
    for i in range(len(df["name"])):
        print(i, "\n")
        differences[i] = {}
        for j, song in enumerate(df["name"]):
            differences[i][j] = len(song) / total_length
            print(differences[i][j])
    
        if (sum(differences[i].values())) < 1:
            differences[i][0] += (1 - sum(differences[i].values()))
        print(differences[i])
        print(sum(differences[i].values()))


    return differences

#1umwX5x9YfdOYZDWR5BjUO

#short
#4V2lefCcuGNzHe0hjvMx1m


#playlist iteration from https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py 



def main():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    #print(scrape_genius_lyrics(["Eminem"], "Rap God"))
    id = get_playlist_id()
    df1, offset = get_playlist_track_info(sp, id)
    print(df1)

    matrix = create_matrix(df1)

    transitioner = SongMarkov(matrix)
    print(transitioner.transition_matrix)
    print(transitioner.indices)

    print(transitioner.get_next_song(0))
    print(transitioner.create_transitions(0))

    
    

if __name__ == "__main__":
    main()
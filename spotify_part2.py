"""
Abby Mueller
"""

import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#import requests
#from bs4 import BeautifulSoup as bs
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
from PIL import Image, ImageDraw, ImageFont
import urllib.request
from pathlib import Path #check if images exist or not
import random

#set environment variables https://phoenixnap.com/kb/set-environment-variable-mac
class SongMarkov:
    """
    Class for implementing a markov chain of songs, based off a transition matrix passed
    during construction. Currently am passing a matrix based off spotify playlist
    """
    def __init__(self, transition_matrix):
        self.transition_matrix = transition_matrix
        self.indices = list(transition_matrix.keys())
    
    def get_next_song(self, curr_song):
        """
        Args: curr_song is index of current song being passed
        """
        return np.random.choice(
            self.indices, 
            p=[self.transition_matrix[curr_song][next_index] for next_index in self.indices]
        )
    
    def create_transitions(self, current_song, len_param=10):
        """
        Args: current song (int) is index of song being examined
        len_param (int) is how many transitions to make
        (default 10)

        returns the list of transitions between songs
        """
        songs = []
        while len(songs) < len_param:
            next_song= self.get_next_song(current_song)
            songs.append(next_song) 
    
        return songs

    

        #markov chain of probabilities of 

def get_playlist_id():
    """
    Seeks user input to get playlist ID
    returns spotify playlist id in Spotipy format
    """
    print("What is the id of the playlist?")
    play_id_num = input()
    
    if play_id_num.startswith("https://open.spotify.com"):
        play_id_num = play_id_num[34:]
    
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
        
            #handle multiple artists
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

        
        offset = offset + len(response['items'])

        return df2, offset

def create_matrix(df):
    """
    Given a df of form id, name, artist,
    creates a transition matrix from the song title lengths.
    """
    #get lengths of each song title, total up
    total_length = 0
    for song in df["name"]:
        total_length += len(song)
    
    differences = {}

    for i in range(len(df["name"])):
        differences[i] = {}
        for j, song in enumerate(df["name"]):
            differences[i][j] = len(song) / total_length
    
        #corrects for floating point rounding yielding a number just under 1
        if (sum(differences[i].values())) < 1:
            differences[i][0] += (1 - sum(differences[i].values()))

    return differences


def get_image(sp,artist_name):
    """
    Using spotipy, gets the image from Spotify associated with artist.
    sp (spotify credentials object)
    artist_name (str) is name artist.
    returns str image URL
    """
    image = ""
    
    name = artist_name
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        image = artist['images'][0]['url']
    
    return image


#sample playlist ids
#1umwX5x9YfdOYZDWR5BjUO

#short
#4V2lefCcuGNzHe0hjvMx1m


#playlist iteration from https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py 
def create_image_art(sp, df1, id, order):
    """
    Creates the image art, using spotify credentials to access images,
    data from provided dataframe (generated in earlier step from spotify)
    and the give order from the markov generator.
    playlist id is to get name to label the art.
    ARgs: sp, spotify credentials
        df1, dataframe of song id/artist/name
        id, playlist id
        order, generated song order 
    Doesn't return anything but rather saves the artist images to be used
    and also saves a final image as final.jpg.
    """
    images = {}
    for i in order:
        images[i] = get_image(sp, df1["artist"][i][0] )
    #current path info stuff came from
    #https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
     
    curr_path = Path(__file__).parent.resolve()
    for key, value in images.items():
        #to save stuff into file 
        full_path = str(curr_path) + "/images/" + str(key) + ".jpg"
        urllib.request.urlretrieve(value, full_path)
    
    plist = sp.playlist(id) #for generated image naming 
    new_base = Image.open(str(curr_path) + "/images/" + str(order[0]) + ".jpg")
    with new_base as background:
        for i in (order):
            img = Image.open(str(curr_path) + "/images/"  + str(i) + ".jpg")
            img = img.convert("RGBA")
            #rgba color replacement
            #https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color 
            data = np.array(img)
            r, g, b, a = data.T
            alpha = random.randint(0, 200)
            
            white_areas = (r == 255) & (b == 255) & (g == 255) & (a == alpha)
            data[..., :-1][white_areas.T] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            img = Image.fromarray(data)
            img.putalpha(alpha)
            
            paste_location_x = random.randint(-200,200) #base is 750 px
            paste_location_y= random.randint(-200,200)
            img = img.rotate(random.randint(0, 360))

            background.paste(img, (paste_location_x,paste_location_y), img)
            temp = background.save(str(curr_path) + "/images/" + str(plist['name']) + ".jpg")

    #in this section we draw the playlist name onto the image
    #could probably have been separate function but alas
    plist = sp.playlist(id)
    
    k = Image.open(str(curr_path) + "/images/" + str(plist['name']) + ".jpg")
    txt = ImageDraw.Draw(k)
    
    #caveat: this works for Mac computers, for windows we would need to do "arial.tff" or somethine else
    fnt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 28, encoding="unic")
    txt.text((100, 100), plist['name'], font=fnt, fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
   
    k.show() #for demo purposes 
    #update and save
    k.save(str(curr_path) + "/images/" + str(plist['name']) + ".jpg")

def main():
    """
    Creates spotify object, then given a playlist id,
    generates a dataframe based off the playlist on Spotify and uses that
    in order to make a transition matrix and later to grab images for the art.
    Creates art based off song frequency using artist images from spotify. 
    """
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    id = get_playlist_id()
    df1, offset = get_playlist_track_info(sp, id)

    matrix = create_matrix(df1)

    #instantiate markov chain
    transitioner = SongMarkov(matrix)
    #starting vector is that any song has a likelihood of being chosen, in order to allow
    #for higher chance of unique images being generated each time
    first_song = np.random.choice(transitioner.indices)
    #15 transitions made
    order = transitioner.create_transitions(first_song, 15)
    
    create_image_art(sp, df1, id, order)
    

if __name__ == "__main__":
    main()
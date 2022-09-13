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


def get_image(sp,artist_name):
    image = ""
    
    name = artist_name
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        image = artist['images'][0]['url']
    
    return image

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
    first_song = np.random.choice(transitioner.indices)

    print(transitioner.get_next_song(0))
        
    order = transitioner.create_transitions(first_song, 12)

    
    images = {}
    for i in order:
        images[i] = get_image(sp, df1["artist"][i][0] )
    print(images)

    #image = Image.open("base.jpg")
    curr_path = Path(__file__).parent.resolve()
    for key, value in images.items():
        #path https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
        #to save stuff into file 
        full_path = str(curr_path) + "/images/" + str(key) + ".jpg"
        urllib.request.urlretrieve(value, full_path)
    
    new_base = Image.open(str(curr_path) + "/images/" + str(order[0]) + ".jpg")

    #now, for each image
    #with Image.open(str(curr_path) + "/base.jpg") as background:
    with new_base as background:
        for i in (order):
            print(str(i))
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
            temp = background.save(str(curr_path) + "/images/final.jpg")
            #background.show()

    plist = sp.playlist(id)
    print(plist['name'])
    
    k = Image.open(str(curr_path) + "/images/final.jpg")
    txt = ImageDraw.Draw(k)
    
    txt.text((100, 100), plist['name'],fill = (255,0,0))
    #txt.text((100, -100), plist['name'], fill =(255,255,255))
   
    k.show()
    k.save(str(curr_path) + "/images/final.jpg")
    


    
    

if __name__ == "__main__":
    main()
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

        #markov chain of probabilities of 


#genius scraping
def scrape_lyrics(artist, song):
    if len(artist) == 1:
        artist = artist[0]
        #print(artistname)
        artistNameNoSpace = str(artist.replace(' ','-')) if ' 'in artist else str(artist)
        songNameNoSpace = str(song.replace(' ','-')) if ' 'in song else str(song)
        page = requests.get('https://genius.com/'+ artistNameNoSpace + '-' + songNameNoSpace + '-' + 'lyrics')
        #print('https://genius.com/'+ artistNameNoSpace + '-' + songNameNoSpace + '-' + 'lyrics')
        html = bs(page.text, 'html.parser')
        lyrics1 = html.find("div", class_="lyrics")
        lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
        if lyrics1:
            lyrics = lyrics1.get_text()[:300]
        elif lyrics2:
            lyrics = lyrics2.get_text()[:300]
        elif lyrics1 == lyrics2 == None:
            lyrics = None
        return lyrics
    elif len(artist) > 1:
        return song

def attach_to_frame(df, artist,i):
    row = df.iloc[i]
    #print(i,row["name"],artist)
    t = scrape_lyrics(artist, row["name"])
    df.loc[i, 'lyrics'] = t
    return df

def sentiment_analysis(df):
    sentences = df['lyrics'].values.tolist()
    #list filter
    #https://www.geeksforgeeks.org/python-remove-none-values-from-list/
    #res = list(filter(lambda item: item is not None, sentences))
 
    #print(sentences)
    analyzer = SentimentIntensityAnalyzer()
    for i, sent in enumerate(sentences):
        if sent == None or sent == "nan" or pd.isna(sent): #handle nonetype sentence for songs with no easily available lyric
            df.loc[i, 'pos'] = 0.0
            continue
        
        #row = df.iloc[i]
        print(sent)
        print(analyzer.polarity_scores(sent))
        pos = analyzer.polarity_scores(sent)['pos']
        #neg = analyzer.polarity_scores(sent)['neg']
        df.loc[i, 'pos'] = pos
        
        #isna https://towardsdatascience.com/5-methods-to-check-for-nan-values-in-in-python-3f21ddd17eed
    
        #from vader
        # https://github.com/cjhutto/vaderSentiment
        
    
    return df

def fix_nan(flt):
    return 0.0 if pd.isna(flt) else flt

def create_matrix(df):
    positivities = df['pos'].values.tolist()
    sum_diff = 0
    sum_diffs = []
    differences = {}
    i = 0
    for val in df['pos']:
        differences[i] = {}
        sum_diff_list = []
        val = fix_nan(val)
        j = 0
        for val2 in df['pos']:
            val2 = fix_nan(val2)
            diff = math.exp(abs(val-val2))
            differences[i][j] = diff
            print(diff,"diff")
            sum_diff += diff
            sum_diff_list.append(diff)
            j += 1
        i += 1 #increment
        sum_diffs.append(sum_diff_list)
    print("sumdiffs", sum_diffs)
    #print("sum----",sum_diff)
    #print(differences)

    matrix = {}
    for k, v in differences.items():
        #print(k,v)
        matrix[k] = {}
        print("sum_diffs k", sum(sum_diffs[k]), "\n")
        for k2, v2 in v.items():
            #print("v[k],v2", v[k], v2)
            diff = v[k] - v2
            num = math.exp(abs(diff))
            #print(diff, num)
            
            percent = num / sum(sum_diffs[k])
            matrix[k][k2] = percent
        #print(k)
        print("totalsum" , sum((sum_diffs[k])))
        print(sum(matrix[k].values()))
    print(matrix)

    return None
    #will be by index in table

def create_differences(df_col): 
    differences = {}
    
    r = 0 #row index
    c = 0 #column index
    while r < len(df_col.keys()): 
        differences[r] = {}
        row = differences[r]
        val = fix_nan(df_col[r])
        #print(r, val)
        
        while c < len(df_col.keys()):
            #if r not in differences:
                #differences[r] = {}
            #row = differences[r]
            val2 = fix_nan(df_col[c])
            diff = math.exp(abs(val - val2))
            row[c] = diff
            #print("diff",diff)
            c += 1
            #print(row)
        c = 0
        r += 1
       
    #print(differences)
    return differences
    
def differences_to_markov(differences):
    for i,d in enumerate(differences):
        reference = differences[i][i]
        sum1= sum(differences[i].values())
        print("Sum is", sum1)
        for j, di in enumerate(differences):
            diff = math.exp(abs(reference - differences[i][j]))
            print("ref, di", reference, di)
            print("curr diff is ", diff)
            new_scaled_dif = diff / sum1
            print("scaled is ", new_scaled_dif)
            differences[i][j] = new_scaled_dif
    
    return differences
    
    


class SongMarkov:
    def __init__(self, transition_matrix):
        self.transition_matrix = transition_matrix
        self.indices = list(transition_matrix.keys())
    
    def get_next_song(self, curr_song):
        return np.random.choice(
            self.indices, 
            p=[self.transition_matrix[curr_song][next_index] for next_index in self.indices]
        )
    
    def create_transitions(self, current_note, len_param=4):
        songs = []
        while len(songs) < len_param:
            next_note = self.get_next_note(current_note)
            songs.append(next_note) #don't need to set melody equal to this
        
        return songs


    

def matrix_2(df_col):
    differences = create_differences(df_col)
    d = differences_to_markov(differences)
    print("d", "\n",d)
    print(sum(d[0].values()))

    return d

    #create art
   
    #choose a random number through len of things 
   
    #

    


        

         
    


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

    #print("lyrics",scrape_lyrics(["Lilyisthatyou"], "Party 22"))
    for i,x in enumerate(df1["artist"]):
        df1 = attach_to_frame(df1, x, i)
        #print(i,x)
        #print(str(i) + ":", df1)
  
    df1 = sentiment_analysis(df1)
    print(df1)
    #print(df1)
    df_pos = df1['pos']
    #create_differences(df_pos)

    d=matrix_2(df1['pos'])

    print(df1['pos'].sum())

    transition = SongMarkov(d)
    print(transition.transition_matrix)
    print(transition.indices)

    print(transition.get_next_song(0))
    
  
    #print("pos", df1['pos'])
    #create_matrix(df1)
   
    
    

if __name__ == "__main__":
    main()
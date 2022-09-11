"""
Abby Mueller
"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup as bs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 


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
        if sent == None: #handle nonetype sentence for songs with no easily available lyric
            continue
        
        #row = df.iloc[i]
        pos = analyzer.polarity_scores(sent)['pos']
        neg = analyzer.polarity_scores(sent)['neg']
        df.loc[i, 'pos'] = pos
        df.loc[i, 'neg'] = neg
        #isna https://towardsdatascience.com/5-methods-to-check-for-nan-values-in-in-python-3f21ddd17eed
        if (pos == 0.0 and neg == 0.0) or pd.isna(pos) or pd.isna(neg):
            df.loc[i, 'pos_neg'] = 0.0
        else:
            df.loc[i, 'pos_neg'] = pos + neg
        
        #from vader
        # https://github.com/cjhutto/vaderSentiment
        
    
    return df

def create_matrix(df):
    return None
    #will be by index in table
    


#1umwX5x9YfdOYZDWR5BjUO
#playlist iteration from https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py 



def main():

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    #print(scrape_genius_lyrics(["Eminem"], "Rap God"))
    id = get_playlist_id()
    df1, offset = get_playlist_track_info(sp, id)

    #print("lyrics",scrape_lyrics(["Lilyisthatyou"], "Party 22"))
    for i,x in enumerate(df1["artist"]):
        df1 = attach_to_frame(df1, x, i)
        #print(i,x)
        #print(str(i) + ":", df1)
  
    df1 = sentiment_analysis(df1)
    #print(df1)
    print("posneg",df1['pos_neg'])
    
    

if __name__ == "__main__":
    main()
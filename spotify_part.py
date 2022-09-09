"""
Abby Mueller
"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup as bs


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

#genius scraping and beautiful soup from https://medium.com/swlh/how-to-leverage-spotify-api-genius-lyrics-for-data-science-tasks-in-python-c36cdfb55cf3
def scrape_genius_lyrics(artistname, song):
    artistname = artistname[0]
    #print(artistname)
    artistNameNoSpace = str(artistname.replace(' ','-')) if ' 'in artistname else str(artistname)
    songNameNoSpace = str(song.replace(' ','-')) if ' 'in song else str(song)
    page = requests.get('https://genius.com/'+ artistNameNoSpace + '-' + songNameNoSpace + '-' + 'lyrics')
    #print('https://genius.com/'+ artistNameNoSpace + '-' + songNameNoSpace + '-' + 'lyrics')
    html = bs(page.text, 'html.parser')
    lyrics1 = html.find("div", class_="lyrics")
    #print(lyrics1)
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    return lyrics

def attachLyricsToFrame(df,artistname ):
    #print(df)
    for i, title in enumerate(df["name"]):
        
        test = scrape_genius_lyrics(artistname, title)
        df.loc[i, 'lyrics'] = test
    
    return df




#1umwX5x9YfdOYZDWR5BjUO
#playlist iteration from https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py 



def main():

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    #print(scrape_genius_lyrics(["Eminem"], "Rap God"))
    print("x")
    id = get_playlist_id()
    df1, offset = get_playlist_track_info(sp, id)
    #print(df1)
    #print(df1.keys())
    finalDf = None
    for x in range(offset):
        row = df1.iloc[x]
        newDf = attachLyricsToFrame(df1, row["artist"])
        if x == offset - 1:
            finalDf = newDf
    
    print(finalDf)
    
    
        
        #attachLyricsToFrame(df1, )

        
    


if __name__ == "__main__":
    main()
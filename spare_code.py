def scrape_lyr(artistname, song):
    if len(artistname) == 1:
        artistname = artistname[0]
        artistNameNoSpace = str(artistname.replace(' ','-')) if ' 'in artistname else str(artistname)
        songNameNoSpace = str(song.replace(' ','-')) if ' 'in song else str(song)
        page = requests.get('https://genius.com/'+ artistNameNoSpace + '-' + songNameNoSpace + '-' + 'lyrics')
        
    else: #len is 2 or greater (idk what happens if this is 3+, will worry later )
        artist2 = artistname[1]
        artistname = artistname[0]
        artistNameNoSpace = str(artistname.replace(' ','-')) if ' 'in artistname else str(artistname)
        artist2NameNoSpace = str(artist2.replace(' ','-')) if ' 'in artist2 else str(artist2)
        songNameNoSpace = str(song.replace(' ','-')) if ' 'in song else str(song)
        page = requests.get('https://genius.com/'+ artistNameNoSpace + '-and-' + artist2NameNoSpace + "-" + songNameNoSpace + '-' + 'lyrics')
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
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
    if lyrics1:
        lyrics = lyrics1.get_text()[:300]
    elif lyrics2:
        lyrics = lyrics2.get_text()[:300]
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    print("lyrics:", lyrics)
    return lyrics

def attachLyricsToFrame(df, artistname ):
    #print(df)
    for title in df["name"]:
        print(title)
        #test = scrape_genius_lyrics(artistname, title)
        test = scrape_lyr(artistname, title)
        df.loc['lyrics'] = test
        print(df.loc['lyrics'])
    
    return df
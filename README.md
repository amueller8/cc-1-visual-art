
# Art of Artists
a spotify playlist-based art generator that uses images of artists you listen to!

## Description

"Art of Artists" uses spotipy, a python API for spotify, to collect information from a playlist you give to it!
Based on the length of the names of songs in your playlist (which were stored in a dataframe using Pandas), a Markov chain is generated which helps pick an ordering of songs from your playlist.
This ordering isn't used for you to jam out to (although you're invited to try to listen to your playlist in that order).
Instead, it guides the ordering of when images of the musical artist of that song are added to a sort of canvas, using Pillow! Each image is unique even if it comes from the same playlist-- the transitions will be different as well as the angle and opacity of images.

## How to use this

If you want to use this to create art on your own, great!
Once you download this code...
You will need to have your own <strong> Spotify developer account </strong> (try going to https://developer.spotify.com/dashboard/, if you don't have an account you will need to login or create one). Once at the dashboard, create a new app. This will give you a `CLIENT_ID` and a `CLIENT_SECRET`.
I didn't hard code in any of these so as to not have it on GitHub (gotta keep things safe!). The following instructions assume you are on a Mac. </br>
Navigate to the folder where this code is via terminal (may take a lot of `cd`s,), this is easier in VSCode.
Then, <strong> run the following code in terminal </strong>:
```
  export SPOTIPY_CLIENT_ID='\<YOURCLIENTIDHERE>'
  export SPOTIPY_CLIENT_SECRET='<\YOURCLIENTSECRET>'
```

Note the lack of spaces between the stuff after export :)

Once you've done this in terminal, you're almost ready to go! <strong> Go to spotify and pick out a playlist you like:</strong>
<p align="center">
<img width="500" alt="Finding Playlist Id" src="https://user-images.githubusercontent.com/68559641/190233078-901db4cc-dced-4444-b2fe-6c6d04729823.png"> <br>
</p>
<strong> Copy </strong> either its url or the sequence of digits/numbers that comes after the playlist/ part of the url.
When you go to create art,<strong> paste this in as the playlist ID! </strong><br>
<p align="center">
<img width="500" alt="Screen Shot 2022-09-14 at 2 27 25 PM" src="https://user-images.githubusercontent.com/68559641/190233621-5f5bd573-c468-4338-9f72-7350eb2eb9cb.png"> <br>
</p>
(Some of the command line chaos is due to the fact that my files are being backed up on OneDrive).

Then, voila, art! <br>
<p align="center">
<img width = "300px" alt = "Hot Hits USA playlist art" src = "https://user-images.githubusercontent.com/68559641/190233839-8656aafa-3f09-492f-99f0-4d01df766fb8.jpg">
 <br>
 </p>

## How is this system personally meaningful to me?

I'm a huge fan of Spotify and listening to music, so it was really fun to incorporate something that I'm passionate about and use and turn it into inspiration for making art! I think it's also fun to actually see some of the ways that musical artists I listen to choose to present themselves-- often, music is an ears-only experience so it's nice to get a visual (if layered) on the people who make it!

## How did I challenge myself as a computer scientist?
<ul>
<li><strong>How did I push myself outside my comfort zone?</strong> </br>
    I used a lot of new things in this project. I had never worked with Spotipy (though I had had a chance to use a Ruby Spotify API), but also experimented a lot for this project and ended up having to cut stuff because it got really complex and there were some frustrating floating point math things going on. I also never really used Pandas or Numpy before. But I explored web scraping a bit (before scrapping it) which was really cool, got to revist Pillow for the first time since Programming with Data, and also had to do a lot of learning/searching for solutions on my own.
</li>
<li><strong>Why was this an important challenge for me?</strong> </br>
  Having to come up with an idea independently and with very little guidance was very new to me, having only really had the chance to do something like that in class once before. I also encountered a lot of stumbling blocks and had to make decisions about what was realistic to pursue and what wasn't. I also had learned about markov chains for the first time so implementing felt like a proof of some understanding.
</li>
<li><strong>Next steps going forward?</strong> </br>
If I have time or can wrap my head around what was happening with floating-point stuff, I would love to return to my original idea which was using sentiment analysis of the lyrics of each song to determine how positive each song in the playlist is, then generating art that revolves around that. I think it would be interesting to juxtapose a playlist, which evokes a mood in a human listener, with a computer's modelled notion of what that emotional experience might be.
</li>

</ul> </br>

### Do I think this system is creative? How or how not?
I think that this system isn't entirely creative but is getting there. 
It definitely introduces ideas of randomness based on resources provided to it, but randomness alone does not equal creativity.
Specifically, one aspect of a computationally creative system we discussed in class that this system doesn't really have is a way to self-filter the art and decide if it is good enough or needs improvement. It does what it is told in the sense that it spits out art! But it does depend on data that is given to it-- it is not yet roaming spotify on its own deciding to make art, or making comparisons of art across playlists.

## Sources

Some sources I consulted were:
https://medium.com/swlh/how-to-leverage-spotify-api-genius-lyrics-for-data-science-tasks-in-python-c36cdfb55cf3   </br>
I did not end up using web scraping but this was really helpful in orienting myself with Spotipy specifically (although I branched out to the Spotipy documentation for playlist-specific workings) as well as how I would turn Spotipy info into a dataframe with pandas, because I had no knowledge of pandas prior. </br>

Knowledge on setting the environment variables (like the CLIENT SECRET) was guided by https://phoenixnap.com/kb/set-environment-variable-mac, because I didn't want to hard-code in the client ID and secret (that's bad practice). </br>
Playlist iteration inspiration came from the Spotipy documentation/examples hosted on github: https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py  

I also referred to a few stackoverflow threads:
https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory helped me save images of artists into an images folder, as well as the final image.
With Pillow, I did some rgba color replacement to alter the artist images in random ways:
https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color inspired by here





import spotipy
from spotipy.oauth2 import SpotifyOAuth
from lyricsgenius import Genius
import os

cId='117934e0aba84892bc39666d4ecdb161'
cSecret='7f4ca2c9fdea41c2877d093124f43961'
uri='https://localhost:8888/callback/'
geniusId='bHhcliIcINMLRr-FlzniYIybs3HL-zcDN341voGkfXyqeKrnUF8ZjNmpXqTRRBi_'

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=cId, client_secret=cSecret, redirect_uri=uri))
results = sp.current_user_saved_tracks()

lyricPath = "/lyrics/"

def getAllArtists(results):
    
    allArtists = []

    for _, item in enumerate(results['items']):
        track = item['track']
        currArtist = track['artists'][0]['name']
        if [currArtist] not in allArtists:
            allArtists.append([currArtist])

    return allArtists

def buildLibrary(results, artists):

    library = artists.copy()

    for _, item in enumerate(results['items']):
        track = item['track']
        currArtist = track['artists'][0]['name']
        for i in range(len(artists)):
            if artists[i][0] == currArtist:
                library[i].append(track['name'])

    sortedLibrary = sortLibrary(library)
    return sortedLibrary

def sortLibrary(unsorted):

    for i in range(len(unsorted)):
        unsorted[i][1:] = sorted(unsorted[i][1:])
    sortedLibrary = sorted(unsorted, key=getArtistName)

    return sortedLibrary

def getArtistName(artist_and_songs):
    return artist_and_songs[0]

def writeLyrics(library):

    baseId = 0
    artistIdx = 0
    genius = Genius(geniusId)
    while artistIdx < len(library):
        currIdx = 1
        currArtist = library[artistIdx][0]
        while currIdx < len(library[artistIdx]):
            currTitle = library[artistIdx][currIdx]
            currLyrics = genius.search_song(currTitle, currArtist)
            file = open(os.getcwd() + lyricPath + str(baseId) + "-" + currArtist.replace(" ","") + "-" + currTitle.replace(" ","") + ".txt", "x")
            file.write(currLyrics.lyrics)
            file.close()
            currIdx += 1
            baseId += 1
        artistIdx += 1

    return

artists = getAllArtists(results)
library = buildLibrary(results, artists)

writeLyrics(library)

print("Program executed successfully")














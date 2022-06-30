import spotipy
import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials
from Recognition import FileManip
from Recognition import APIs


def getSpotify():
    auth_manager = SpotifyClientCredentials(client_id=APIs.apiKeys["Spotify API Key"],
                                            client_secret=APIs.apiKeys["Spotify API Secret"])
    return spotipy.Spotify(auth_manager=auth_manager)


def getSongURISpotify(songName, artist):
    spotify = getSpotify()
    results = spotify.search(q='track:' + songName + ' artist:' + artist, type='track')
    try:
        return results['tracks']['items'][0]['uri']
    except Exception as e:
        print(results)
        print("Error:", e)
        return None

def getSongEnergySpotify(songURI):
    spotify = getSpotify()
    song = spotify.audio_features(songURI)
    try:
        return song[0]['energy']
    except Exception as e:
        print(song)
        print("Error:", e)
        return None
def getSongAlbumSpotify(songURI):
    spotify = getSpotify()
    song = spotify.track(songURI)
    return song['album']['name']

def getSongGenreSpotify(songURI):
    spotify = getSpotify()
    songAlbumUri = spotify.track(songURI)['album']['uri']
    songAlbum = spotify.album(songAlbumUri)
    albumGenre = songAlbum['genres']
    if albumGenre == []:
        return None
    else:
        return albumGenre

def getSongGenreAudioDB(songName, artist):
    url = "https://theaudiodb.p.rapidapi.com/searchtrack.php"

    querystring = {"s": artist, "t": songName}

    headers = {
        "X-RapidAPI-Key": APIs.apiKeys["Rapid API Key"],
        "X-RapidAPI-Host": "theaudiodb.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        return response.json()['track'][0]['strGenre']
    except Exception as e:
        print(response)
        print("Error:", e)
        return None

def getSongGenreShazam(songName):

    searchUrl = "https://shazam.p.rapidapi.com/search"

    querystring = {"term": songName, "locale": "en-US", "offset": "0", "limit": "5"}

    headers = {
        "X-RapidAPI-Key": APIs.apiKeys["Rapid API Key"],
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

    response = requests.request("GET", searchUrl, headers=headers, params=querystring)
    songKey = response.json()['tracks']['hits'][0]['track']['key']

    detailsUrl = "https://shazam.p.rapidapi.com/songs/get-details"

    querystring = {"key": songKey, "locale": "en-US"}

    response = requests.request("GET", detailsUrl, headers=headers, params=querystring)

    if "genre" in response.json():
        return response.json()['genres']['primary']
    else:
        return None

def autoFillDetails(songDir, songName, artist, genre = None):
    energy = getSongEnergySpotify(getSongURISpotify(songName, artist))
    album = getSongAlbumSpotify(getSongURISpotify(songName, artist))
    if genre == None:
        genre = getSongGenreSpotify(getSongURISpotify(songName, artist))
        if genre == None:
            print("No genre found for " + songName + " in the Spotify database, trying AudioDB...")
            genre = getSongGenreAudioDB(songName, artist)
            if genre == None:
                print("No genre found for " + songName + " in the AudioDB database, trying Shazam...")
                genre = getSongGenreShazam(songName)
                if genre == None:
                    print("No genre found for " + songName + " in the Shazam database, genre detection failed :( \n")
                    genre = '' # If no genre is found, set it to empty string
    print("Filling in details for " + songName + " by " + artist + "...")
    FileManip.editMp3Details(songDir, artist, album, songName, genre, str(energy))
    print("Done!")

def test(songName, artist):
    pass


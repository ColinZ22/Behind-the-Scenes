import spotipy
import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials
from Recognition import FileManip

auth_manager = SpotifyClientCredentials(client_id="671865bb1aa942d89f8461cb1dcfdbbb",
                                        client_secret="82a9fba6ed3749579106ceb8de478dc4")
spotify = spotipy.Spotify(auth_manager=auth_manager)

def getSongURISpotify(songName, artist):
    results = spotify.search(q='track:' + songName + ' artist:' + artist, type='track')
    try:
        return results['tracks']['items'][0]['uri']
    except Exception as e:
        print(results)
        print("Error:", e)
        return None

def getSongEnergySpotify(songURI):
    song = spotify.audio_features(songURI)
    try:
        return song[0]['energy']
    except Exception as e:
        print(song)
        print("Error:", e)
        return None
def getSongAlbumSpotify(songURI):
    song = spotify.track(songURI)
    return song['album']['name']

def getSongGenreSpotify(songURI):
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
        "X-RapidAPI-Key": "0d23d67a85msh4135704ba68fb5fp1cbfbajsn1d1390403884",
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
        "X-RapidAPI-Key": "0d23d67a85msh4135704ba68fb5fp1cbfbajsn1d1390403884",
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

    response = requests.request("GET", searchUrl, headers=headers, params=querystring)
    songKey = response.json()['tracks']['hits'][0]['track']['key']


    detailsUrl = "https://shazam.p.rapidapi.com/songs/get-details"

    querystring = {"key": songKey, "locale": "en-US"}

    headers = {
        "X-RapidAPI-Key": "0d23d67a85msh4135704ba68fb5fp1cbfbajsn1d1390403884",
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

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


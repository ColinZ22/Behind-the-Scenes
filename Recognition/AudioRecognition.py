import requests
import sys, base64
import hashlib
import hmac
import os
import time
from pydub import AudioSegment
import fleep
from shazamio import Shazam
from Recognition import APIs

def isFakeMp3(songDir):
    info = fleep.get(open(songDir, "rb").read(128))
    if info.extension != ['mp3']:
        print("Error when Trimming Song, fake mp3 file detected!!!!")
        print(songDir, "contains", info.extension, "data, booooooo get exposed")
        return True
    else:
        return False

def trimSong(songDir,
             tempFileDir= os.getcwd() + "\Temp",
             startTimeSeconds=0,
             endTimeSeconds=8):
    try:
        song = AudioSegment.from_mp3(songDir)
    except Exception as e:
        print("Error when trimming song:", e)
        return None
    else:
        startTimeMiliSeconds = startTimeSeconds * 1000
        endTimeMiliSeconds = endTimeSeconds * 1000
        trimmedSong = song[startTimeMiliSeconds:endTimeMiliSeconds]
        trimmedSong.export(f"{tempFileDir}\\trimmedSong.mp3", format="mp3")
        return f"{tempFileDir}\\trimmedSong.mp3"

def importSongStream(songDir):
    return open(songDir, 'rb').read()

def importSongBase64(songDir):
    songStream = open(songDir, 'rb')
    songBase64 = base64.b64decode(songStream.read())
    songStream.close()
    return songBase64

def getSongNameAudd(songDir):

    results = {}

    data = {
        'api_token': APIs.apiKeys["Audd API Token"],
        'return': 'apple_music,spotify',
    }
    try:
        files = {
            'file': importSongStream(trimSong(songDir))
        }
    except:
        return None

    response = requests.post('https://api.audd.io/', data=data, files=files)

    try:
        results['songName'] = response.json()['result']['title']
        results['artistName'] = response.json()['result']['artist']
        results['songGenre'] = response.json()['result']['genreNames']
        return results
    except Exception as e:
        print(response)
        print("Error:", e)
        return None

def getSongNameACRCloud(songDir):

    results = {}

    access_key = APIs.apiKeys["ACRCloud Access Key"]
    access_secret = APIs.apiKeys[ "ACRCloud API Access Secret"]
    requrl = "http://identify-eu-west-1.acrcloud.com/v1/identify"

    http_method = "POST"
    http_uri = "/v1/identify"

    # change data_type to "fingerprint" if want to identify fingerprint instead of audio file
    data_type = "audio"
    signature_version = "1"
    timestamp = time.time()

    string_to_sign = http_method + "\n" + http_uri + "\n" + access_key + "\n" + data_type + "\n" + signature_version + "\n" + str(
        timestamp)

    sign = base64.b64encode(hmac.new(access_secret.encode('ascii'), string_to_sign.encode('ascii'),
                                     digestmod=hashlib.sha1).digest()).decode('ascii')

    try:
        sample_bytes = os.path.getsize(trimSong(songDir))
    except:
        return None

    files = [
        ('sample', ('file.mp3', open(trimSong(songDir), 'rb'), 'audio/mpeg'))
    ]
    data = {'access_key': access_key,
            'sample_bytes': sample_bytes,
            'timestamp': str(timestamp),
            'signature': sign,
            'data_type': data_type,
            "signature_version": signature_version}

    response = requests.post(requrl, files=files, data=data)

    try:
        results['songName'] = response.json()['metadata']['music'][0]['title']
        results['artistName'] = response.json()['metadata']['music'][0]['artists'][0]['name']
        results['songGenre'] = response.json()['metadata']['music'][0]['genres'][0]['name']
        return results
    except Exception as e:
        print(response)
        print("Error:", e)
        return None

# Not used, but can be used as a backup method
def getSongNameShazam(songDir):

    url = "https://shazam-core.p.rapidapi.com/v1/tracks/recognize"

    # payload = importSongStream(songDir)
    payload = importSongStream(trimSong(songDir))
    headers = {
        "content-type": "multipart/form-data; boundary=---011000010111000001101001",
        "X-RapidAPI-Key": APIs.apiKeys["Rapid API Key"],
        "X-RapidAPI-Host": "shazam-core.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

def autoSongRecognition(songDir):

    print("Checking file...")
    if isFakeMp3(songDir):
        return None
    else:
        print("Starting auto song recognition (utilizing all available services)...")
        songMetadata = getSongNameACRCloud(songDir)
        if songMetadata == "Fake MP3 File!!!":
            return None
        if songMetadata == "" or songMetadata == None:
            print("ACRCloud failed to recognize the song, falling back to Audd...")
            songName = getSongNameAudd(songDir)
            if songMetadata == "" or songMetadata == None:
                print("Song Recognition failed :( \n")
                return None
        return songMetadata

def test(songDir):
    pass
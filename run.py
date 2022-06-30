import sys

from Recognition import AudioRecognition
from Recognition import SongDetails
from Recognition import FileManip
from Recognition import APIs
import os

completedSongs = {}
errerSongs = {}

def audioProcess(dir):  # dir is the directory of the songs to be processed
    for files in os.listdir(dir):
        filename, file_extension = os.path.splitext(files)
        if file_extension.lower() == '.mp3':
            try:
                songDir = dir + "/" + filename + file_extension
                metaData = AudioRecognition.autoSongRecognition(songDir)
                if metaData == None:
                    errerSongs[filename] = "Song Recognition failed"
                else:
                    SongDetails.autoFillDetails(songDir, metaData['songName'], metaData['artistName'], metaData['songGenre'])
                    completedSongs[filename] = {'songName': metaData['songName']}

            except Exception as e:
                errerSongs[filename + file_extension] = e
        else:
            continue

if __name__ == '__main__':

    APIs.getAPIKeys()

    if len(sys.argv) == 1:
        print("Please provide a directory of songs to be processed")
        dir = input("Full Path to Folder: ").strip()
    else:
        dir = sys.argv[1].strip()

    audioProcess(dir)
    print("Songs processed: ", len(completedSongs))
    print(completedSongs)
    print("Songs failed: ", len(errerSongs))
    print(errerSongs)
    if os.path.exists(r"Temp\trimmedSong.mp3"):
        os.remove(r"Temp\trimmedSong.mp3")
    if os.path.exists(r".cache"):
        os.remove(r".cache")
    print("\nOperation Complete.")

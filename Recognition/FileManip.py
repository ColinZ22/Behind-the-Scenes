import eyed3
import os

def editMp3Details(songDir, artist, album, title, genre, energy):
    # suppress useless warnings
    eyed3.log.setLevel("ERROR")

    file = eyed3.load(songDir)
    file.tag.artist = artist
    file.tag.album = album
    file.tag.album_artist = artist
    file.tag.title = title
    file.tag.genre = genre
    file.tag.publisher = energy
    file.tag.save()

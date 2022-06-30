# Behind-the-Scenes
- MP3 File Music Recognition (Primary: ACRCloud API, Backup: Audd API)
- Automatically fetches and edits MP3 file metadata based on song recognition results from Spotify and Apple Music Databases.
- Simple command-line interface: give it a Folder Path, and the code will do the rest!

## ***Before You Start...***
- Make sure you have [ffmpeg](https://ffmpeg.org/) installed!
- Make sure you have all required python packages installed!
  - you'll need [pip](https://pip.pypa.io/en/stable/)
  - Clone the repository
  - Open command-line and navigate to the "Behind-the-Scenes" directory
  - Install all required python packages using `pip install -r requirements.txt`

## API Keys
- This project relies on the following 3rd-party APIs:
  - [Spotify](https://developer.spotify.com/dashboard/overview/)
  - [AudD](https://audd.io/)
  - [ACRCloud](https://www.acrcloud.com/)
  - [AudioDB (Thru RapidAPI)](https://rapidapi.com/theaudiodb/api/theaudiodb)
  - [Shazam (Thru RapidAPI)](https://rapidapi.com/apidojo/api/shazam/)
- Click on each of the above links and register **FREE** accounts to get your own API keys.
- Keep in mind that some of them will expire after a certain period of time.

## Jeez that's a lot of work...
### - *You're Welcome*

## Ok How Do I Actually Use This Thing??
1. Clone the repository
2. Open command-line and navigate to the "Behind-the-Scenes" directory
3. Run the code by typing in `python run.py`
4. Enter your API Keys, they will be stored locally in *APIKeys.json* within the Behind-the-Scenes directory.
5. Enter the full path to the folder containing the mp3 files to be processed.
6. The code will do the rest!


### YAY this works soooo well I love it!
-- *says no one probably since this is still an early version and a work in progress*
### If you run into any bugs, have suggestions, or personal questions, feel free to reach me at 
[HQ@mail.nasa.gov](mailto:KelinZ2@illinois.edu)
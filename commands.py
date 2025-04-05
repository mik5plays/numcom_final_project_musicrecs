from API_KEYS import SECRET, API_KEY, GENIUS_ACCESS_TOKEN # a file that i won't upload for obvious reasons
from PIL import Image, ImageTk
from io import BytesIO
import pylast
import requests
import tkinter as tk
from lyricsgenius import Genius

from pprint import pprint

ROOT_URL = 'http://ws.audioscrobbler.com/2.0/'

genius = Genius(GENIUS_ACCESS_TOKEN)
genius.verbose = False # turn off status msgs

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=SECRET
)

def get_track_info(artist, track):
    params = {
        'method': 'track.getInfo',
        'api_key': API_KEY,
        'artist': artist,
        'track': track,
        'format': 'json'
    }

    response = requests.get(ROOT_URL, params)

    if response.status_code == 200: # Success
        data = response.json()
        # pprint(data)

        image_url = data['track']['album']['image'][-2]['#text'] if 'album' in data['track'] else "-"
        track_title = data['track']['name']
        album_title = data['track']['album']['title'] if 'album' in data['track'] else "-"
        track_artist = data['track']['artist']['name']
        top_tags = [entry['name'] for entry in data['track']['toptags']['tag']]

        return image_url, track_title, album_title, track_artist, top_tags

    else:
        print(f"Error: {response.status_code}")

def get_similar_track_info(artist, track, n=8):
    params = {
        'method': 'track.getSimilar',
        'api_key': API_KEY,
        'artist': artist,
        'track': track,
        'format': 'json'
    }

    response = requests.get(ROOT_URL, params)

    if response.status_code == 200: # Success
        data = response.json()

        # pprint(data)

        # get first eight similar tracks, unless specified.
        return [track for track in data['similartracks']['track']][:n]

    else:
        print(f"Error: {response.status_code}")

def search_for_tracks(query, n=3):
    params = {
        'method': 'track.search',
        'api_key': API_KEY,
        'track': query,
        'format': 'json'
    }

    response = requests.get(ROOT_URL, params)

    if response.status_code == 200:
        # only want top three most relevant, so:
        data = response.json()
        return [track for track in data['results']['trackmatches']['track']][:n]
    else:
        print(f"Error: {response.status_code}")

def get_lyrics(artist, track):
    song = genius.search_song(track, artist)
    return song.lyrics[song.lyrics.find("["):]

def get_artist_info(query):
    params = {
        'method': 'artist.getInfo',
        'api_key': API_KEY,
        'artist': query,
        'format': 'json'
    }

    response = requests.get(ROOT_URL, params)

    if response.status_code == 200: # Success
        data = response.json()

        url = data['artist']['image'][-2]['#text']
        artist = data['artist']['name']
        tags = [tag['name'] for tag in data['artist']['tags']['tag']]

        return url, artist, tags

    else:
        print(f"Error: {response.status_code}")

def get_similar_artist_info(artist, n=8):
    params = {
        'method': 'artist.getSimilar',
        'api_key': API_KEY,
        'artist': artist,
        'format': 'json'
    }

    response = requests.get(ROOT_URL, params)

    if response.status_code == 200: # Success
        data = response.json()

        return [artist for artist in data['similarartists']['artist']][:n]

    else:
        print(f"Error: {response.status_code}")

def search_for_artists(query, n=3):
    params = {
        'method': 'artist.search',
        'api_key': API_KEY,
        'artist': query,
        'format': 'json'
    }

    response = requests.get(ROOT_URL, params)

    if response.status_code == 200:
        # only want top three most relevant, so:
        data = response.json()
        return [artist for artist in data['results']['artistmatches']['artist']][:n]
    else:
        print(f"Error: {response.status_code}")




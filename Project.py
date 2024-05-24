from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import webbrowser
import time

# Load environment variables
load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

# Function to get the Spotify API token
def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    result.raise_for_status()  # Raises an error for bad responses
    json_result = result.json()
    token = json_result["access_token"]
    return token

# Function to get authorization header
def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# Function to search for an artist by name
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    result.raise_for_status()  # Raises an error for bad responses
    json_result = result.json()["artists"]["items"]
    if not json_result:
        print("No artist with this name exists....")
        return None

    return json_result[0]

# Function to get the top tracks of an artist by artist ID and country code
def get_songs_by_artist(token, artist_id, country_code="IN"):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country_code}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    result.raise_for_status()  # Raises an error for bad responses
    json_result = result.json()["tracks"]
    return json_result

# Function to display the tracks
def display_tracks(tracks):
    for idx, track in enumerate(tracks[:100], start=1):
        print(f"{idx}. {track['name']}")

# Function to open the tracks in Spotify after a delay
def open_tracks_in_spotify_after_delay(tracks):
    time.sleep(3)  # Delay of 3 seconds
    for track in tracks[:5]:
        track_uri = track["uri"]
        webbrowser.open(f"spotify:track:{track_uri.split(':')[-1]}")

# Main code to search for an artist and get their top tracks
token = get_token()
result = search_for_artist(token, "Mohit Lalwani")
if result:
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id, "IN")
    display_tracks(songs)
    open_tracks_in_spotify_after_delay(songs)
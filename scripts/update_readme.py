import os
import requests
from datetime import datetime

README_FILE = "README.md"

def get_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise Exception("Missing Spotify credentials.")

    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret)
    )

    data = resp.json()
    if "access_token" not in data:
        raise Exception(f"Auth failed: {data}")

    return data["access_token"]

def get_top_tracks(token, playlist_id, count=5):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={count}"
    resp = requests.get(url, headers=headers)
    tracks = []

    for item in resp.json().get("items", []):
        track = item.get("track", {})
        name = track.get("name")
        url = track.get("external_urls", {}).get("spotify", "#")
        artists = ", ".j

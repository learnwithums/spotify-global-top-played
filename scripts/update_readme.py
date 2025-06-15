import os, requests
from bs4 import BeautifulSoup
from datetime import datetime

# Spotify config
SPOTIFY_PLAYLIST = "37i9dQZEVXbMDoHDwVN2tF"

def get_spotify_token():
    r = requests.post("https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(os.getenv("SPOTIFY_CLIENT_ID"), os.getenv("SPOTIFY_CLIENT_SECRET")))
    return r.json()["access_token"]

def get_top_spotify_track(token):
    r = requests.get(f"https://api.spotify.com/v1/playlists/{SPOTIFY_PLAYLIST}",
                     headers={"Authorization": f"Bearer {token}"})
    top = r.json()["tracks"]["items"][0]["track"]
    return {
        "name": top["name"],
        "artist": top["artists"][0]["name"],
        "url": top["external_urls"]["spotify"]
    }

def scrape_kworb_top_streams():
    url = "https://kworb.net/spotify/country/global_daily.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    first_row = soup.select_one("table tr:nth-of-type(2)")
    cols = first_row.find_all("td")
    title = cols[1].text.strip()
    artist = cols[1].text.split("–")[0].strip()
    streams = cols[3].text.strip().replace(",", "")
    return {"title": title, "artist": artist, "streams": int(streams)}

def generate_readme(track, stats):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# 🌍 Today’s Most Played Song Globally — {now}\n\n")
        f.write(f"🎧 **{track['name']}** by **{track['artist']}**\n\n")
        f.write(f"🔢 **Estimated streams today:** ~{stats['streams']:,}\n\n")
        f.write(f"[▶️ Listen on Spotify]({track['url']})\n\n")
        f.write(f"🕒 Updated: {now}\n")

def main():
    token = get_spotify_token()
    top = get_top_spotify_track(token)
    stats = scrape_kworb_top_streams()
    generate_readme(top, stats)

if __name__ == "__main__":
    main()

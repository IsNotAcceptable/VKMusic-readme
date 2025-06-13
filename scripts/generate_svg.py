import os
import requests
from datetime import datetime

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = "assets/lastfm_widget.svg"

def get_track():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    try:
        data = requests.get(url).json()
        track = data["recenttracks"]["track"][0]
        return {
            "name": track["name"],
            "artist": track["artist"]["#text"],
            "now": "@attr" in track and "nowplaying" in track["@attr"]
        }
    except:
        return None

def create_svg(track):
    return f'''<svg width="300" height="80" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#9400D3" rx="5"/>
    <text x="20" y="30" font-family="Arial" font-size="14" fill="white">
        {track["name"][:20]}{"..." if len(track["name"]) > 20 else ""}
    </text>
    <text x="20" y="50" font-family="Arial" font-size="12" fill="#EEE">
        {track["artist"][:20]}{"..." if len(track["artist"]) > 20 else ""}
    </text>
    <text x="20" y="70" font-family="Arial" font-size="10" fill="#DDD">
        {"▶ Сейчас играет" if track["now"] else "⏱ " + datetime.now().strftime("%H:%M")}
    </text>
</svg>'''

if __name__ == "__main__":
    track = get_track() or {
        "name": "Не удалось загрузить",
        "artist": "Проверьте настройки",
        "now": False
    }
    os.makedirs("assets", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(create_svg(track))

import os
import requests
from datetime import datetime

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
SVG_TEMPLATE_PATH = "scripts/template.svg"
OUTPUT_SVG_PATH = "docs/lastfm-widget.svg"

def get_track_info():
    """Получает данные из Last.fm API"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    response = requests.get(url)
    data = response.json()
    
    track = data["recenttracks"]["track"][0]
    is_now_playing = "@attr" in track and track["@attr"]["nowplaying"] == "true"
    
    return {
        "track": track["name"],
        "artist": track["artist"]["#text"],
        "status": "Сейчас играет" if is_now_playing else f"Обновлено: {datetime.now().strftime('%H:%M')}",
        "image": track.get("image", [{}])[-1].get("#text", "")
    }

def generate_svg(track_data):
    """Генерирует SVG из шаблона"""
    with open(SVG_TEMPLATE_PATH, "r") as f:
        svg = f.read()
    
    return svg \
        .replace("{{TRACK}}", track_data["track"]) \
        .replace("{{ARTIST}}", track_data["artist"]) \
        .replace("{{STATUS}}", track_data["status"])

if __name__ == "__main__":
    track = get_track_info()
    svg_content = generate_svg(track)
    
    with open(OUTPUT_SVG_PATH, "w") as f:
        f.write(svg_content)

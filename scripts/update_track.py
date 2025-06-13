import os
import requests
from datetime import datetime
from urllib.parse import quote

# Конфигурация
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = "../assets/lastfm_widget.svg"

def get_track_info():
    """Получаем данные о текущем треке"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    response = requests.get(url)
    data = response.json()
    
    track = data["recenttracks"]["track"][0]
    is_now_playing = "@attr" in track and track["@attr"]["nowplaying"] == "true"
    
    return {
        "track": track["name"][:30] + ("..." if len(track["name"]) > 30 else ""),
        "artist": track["artist"]["#text"][:30] + ("..." if len(track["artist"]["#text"]) > 30 else ""),
        "status": "Сейчас играет" if is_now_playing else f"Обновлено: {datetime.now().strftime('%H:%M')}",
        "image": track.get("image", [{}])[-1].get("#text", "")
    }

def create_svg(track_data):
    """Генерируем SVG с данными о треке"""
    return f'''<svg width="350" height="100" viewBox="0 0 350 100" xmlns="http://www.w3.org/2000/svg">
    <style>
        .background {{ fill: #1ed760; rx: 6px; }}
        .text {{ font-family: 'Segoe UI', Arial, sans-serif; fill: white; }}
        .track {{ font-size: 16px; font-weight: 600; }}
        .artist {{ font-size: 14px; }}
        .status {{ font-size: 12px; }}
        .logo {{ font-size: 10px; font-weight: bold; }}
    </style>
    
    <rect width="100%" height="100%" class="background" rx="6"/>
    
    <text x="15" y="30" class="text track">{track_data["track"]}</text>
    <text x="15" y="50" class="text artist">{track_data["artist"]}</text>
    <text x="15" y="80" class="text status">{track_data["status"]}</text>
    <text x="310" y="95" class="text logo">Last.fm</text>
    
    {(f'<image href="{track_data["image"]}" x="250" y="15" width="70" height="70" preserveAspectRatio="xMidYMid meet"/>' 
     if track_data["image"] else '')}
</svg>'''

if __name__ == "__main__":
    track = get_track_info()
    svg_content = create_svg(track)
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

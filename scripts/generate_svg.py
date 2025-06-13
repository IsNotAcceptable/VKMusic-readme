import os
import requests
from datetime import datetime
from urllib.parse import quote

# Конфигурация
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '../assets/lastfm_widget.svg')

def get_track_info():
    """Получаем данные трека с Last.fm"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        track = data["recenttracks"]["track"][0]
        
        return {
            "track": track["name"][:25] + ("..." if len(track["name"]) > 25 else ""),
            "artist": track["artist"]["#text"][:25] + ("..." if len(track["artist"]["#text"]) > 25 else ""),
            "status": "▶ Сейчас играет" if "@attr" in track and track["@attr"]["nowplaying"] == "true" else f"⏱ Обновлено: {datetime.now().strftime('%H:%M')}",
            "cover": track["image"][-1]["#text"] if track.get("image") else None
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_svg(track_data):
    """Генерируем SVG с обложкой"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="120" viewBox="0 0 400 120" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <defs>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="2" dy="2" stdDeviation="2" flood-color="#00000080"/>
        </filter>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#9400D3"/>
            <stop offset="100%" stop-color="#7E00B5"/>
        </linearGradient>
    </defs>

    <rect width="100%" height="100%" fill="url(#bg)" rx="6"/>

    <!-- Обложка -->
    {f'<image href="{track_data["cover"]}" x="10" y="10" width="100" height="100" filter="url(#shadow)" preserveAspectRatio="xMidYMid meet"/>' 
     if track_data["cover"] else 
     '<rect x="10" y="10" width="100" height="100" fill="#6A0099" rx="4"/>'}

    <!-- Текст -->
    <text x="125" y="35" font-family="Arial" font-size="16" font-weight="600" fill="white">
        {track_data["track"]}
    </text>
    <text x="125" y="60" font-family="Arial" font-size="14" fill="#EEE">
        {track_data["artist"]}
    </text>
    <text x="125" y="85" font-family="Arial" font-size="12" fill="#DDD">
        {track_data["status"]}
    </text>
</svg>'''

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    track = get_track_info() or {
        "track": "Трек не найден",
        "artist": "Проверьте настройки",
        "status": "Ошибка подключения",
        "cover": None
    }
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(generate_svg(track))

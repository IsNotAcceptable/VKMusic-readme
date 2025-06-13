import os
import sys
import requests
from datetime import datetime
import base64

# Конфигурация
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
TIMESTAMP = sys.argv[1] if len(sys.argv) > 1 else "0"
OUTPUT_PATH = "assets/lastfm_widget.svg"

def download_image(url):
    """Загрузка и кодирование обложки"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"data:image/jpeg;base64,{base64.b64encode(response.content).decode('utf-8')}"
        return None
    except Exception:
        return None

def get_track_info():
    """Получение данных о текущем треке"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        track = data["recenttracks"]["track"][0]
        
        # Получаем лучшую доступную обложку
        cover_url = next(
            (img["#text"] for img in reversed(track["image"]) 
             if img.get("#text") and "placeholder" not in img["#text"].lower()),
            None
        )
        
        return {
            "name": track.get("name", "Неизвестный трек")[:25],
            "artist": track["artist"].get("#text", "Неизвестный исполнитель")[:25],
            "now_playing": track.get("@attr", {}).get("nowplaying", "false") == "true",
            "cover": download_image(cover_url) if cover_url else None
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_svg(track):
    """Генерация SVG с обложкой"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated: {datetime.now().isoformat()} -->
<!-- Version: {TIMESTAMP} -->
<svg width="450" height="150" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <defs>
        <clipPath id="coverClip">
            <rect x="20" y="20" width="110" height="110" rx="8"/>
        </clipPath>
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#9400D3"/>
            <stop offset="100%" stop-color="#6A0099"/>
        </linearGradient>
    </defs>
    
    <rect width="100%" height="100%" fill="url(#bgGradient)" rx="8"/>
    
    {f'<image href="{track["cover"]}" x="20" y="20" width="110" height="110" clip-path="url(#coverClip)"/>' 
     if track["cover"] else 
     '<rect x="20" y="20" width="110" height="110" fill="#4B0082" rx="8"/><text x="75" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="white">No cover</text>'}
    
    <text x="150" y="40" font-family="Arial" font-size="18" font-weight="bold" fill="white">
        {track["name"]}{"..." if len(track["name"]) >= 25 else ""}
    </text>
    <text x="150" y="70" font-family="Arial" font-size="16" fill="#EEE">
        {track["artist"]}{"..." if len(track["artist"]) >= 25 else ""}
    </text>
    <text x="150" y="100" font-family="Arial" font-size="14" fill="#DDD">
        {"▶ Сейчас играет" if track["now_playing"] else "⏱ " + datetime.now().strftime("%H:%M")}
    </text>
</svg>'''

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    track = get_track_info() or {
        "name": "Нет данных", 
        "artist": "Проверьте настройки",
        "now_playing": False,
        "cover": None
    }
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(create_svg(track))
    print(f"✅ Виджет сгенерирован (v{TIMESTAMP})")

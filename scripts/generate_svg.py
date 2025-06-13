import os
import sys
import requests
from datetime import datetime

# Конфигурация
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
VERSION = sys.argv[1] if len(sys.argv) > 1 else "0"
OUTPUT_PATH = f"assets/lastfm_widget_{VERSION}.svg"

def get_track_info():
    """Получаем данные о текущем треке"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        track = data["recenttracks"]["track"][0]
        return {
            "name": track.get("name", "Неизвестный трек"),
            "artist": track["artist"].get("#text", "Неизвестный исполнитель"),
            "now_playing": track.get("@attr", {}).get("nowplaying", False),
            "cover": track["image"][-1]["#text"] if track.get("image") else None
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_svg(track):
    """Генерируем SVG"""
    return f'''<svg width="400" height="150" xmlns="http://www.w3.org/2000/svg">
    <!-- Версия: {VERSION} -->
    <rect width="100%" height="100%" fill="#9400D3" rx="6"/>
    {f'<image href="{track["cover"]}" x="20" y="20" width="110" height="110"/>' if track["cover"] else ''}
    <text x="150" y="40" font-family="Arial" font-size="16" fill="white">{track["name"]}</text>
    <text x="150" y="70" font-family="Arial" font-size="14" fill="#EEE">{track["artist"]}</text>
    <text x="150" y="100" font-family="Arial" font-size="12" fill="#DDD">
        {"▶ Сейчас играет" if track["now_playing"] else "⏱ " + datetime.now().strftime("%H:%M")}
    </text>
</svg>'''

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    track_data = get_track_info() or {
        "name": "Нет данных", 
        "artist": "Проверьте настройки",
        "now_playing": False,
        "cover": None
    }
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(create_svg(track_data))
    print(f"✅ Виджет сгенерирован (v{VERSION})")

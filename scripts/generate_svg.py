import os
import requests
from datetime import datetime

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = "assets/lastfm_widget.svg"

def get_track_info():
    """Получаем данные трека"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    try:
        print("⌛ Запрос данных из Last.fm...")
        response = requests.get(url, timeout=10)
        data = response.json()
        track = data["recenttracks"]["track"][0]
        
        print(f"🎵 Трек: {track.get('name')} - {track['artist']['#text']}")
        print(f"🖼️ Обложка: {track['image'][-1]['#text']}")
        
        return {
            "name": track["name"],
            "artist": track["artist"]["#text"],
            "cover": track["image"][-1]["#text"],
            "now_playing": "@attr" in track
        }
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return None

def create_svg(track):
    """Генерируем SVG"""
    return f'''<svg width="400" height="150" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#9400D3" rx="6"/>
    <image href="{track['cover']}" x="20" y="20" width="110" height="110"/>
    <text x="150" y="40" font-family="Arial" fill="white">{track["name"]}</text>
    <text x="150" y="70" font-family="Arial" fill="#EEE">{track["artist"]}</text>
</svg>'''

if __name__ == "__main__":
    print("\n=== Генерация виджета ===")
    os.makedirs("assets", exist_ok=True)
    track = get_track_info() or {
        "name": "Нет данных", 
        "artist": "Проверьте настройки",
        "cover": "",
        "now_playing": False
    }
    
    with open(OUTPUT_PATH, "w") as f:
        f.write(create_svg(track))
    print("✅ Готово!")

import os
import requests
from datetime import datetime

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = "assets/lastfm_widget.svg"

def get_track_info():
    """Получаем данные трека с обложкой"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "recenttracks" not in data or not data["recenttracks"]["track"]:
            return None
            
        track = data["recenttracks"]["track"][0]
        return {
            "name": track.get("name", "Неизвестный трек"),
            "artist": track["artist"].get("#text", "Неизвестный исполнитель"),
            "now_playing": track.get("@attr", {}).get("nowplaying", "false") == "true",
            "image": track.get("image", [{}])[-1].get("#text", "")
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    
    return None

def create_svg(track_data):
    """Генерируем минималистичный SVG"""
    track = track_data or {
        "name": "Нет данных о треке",
        "artist": "Проверьте настройки Last.fm",
        "now_playing": False,
        "image": ""
    }
    
    return f'''<svg width="500" height="100" xmlns="http://www.w3.org/2000/svg">
    <!-- Обложка альбома -->
    {f'<image href="{track["image"]}" x="0" y="0" width="100" height="100" preserveAspectRatio="xMidYMid slice"/>' if track["image"] else ''}
    
    <!-- Информация о треке -->
    <text x="120" y="40" font-family="Arial" font-size="18" fill="#333" font-weight="bold">
        {track["name"][:25]}{"..." if len(track["name"]) > 25 else ""}
    </text>
    <text x="120" y="65" font-family="Arial" font-size="16" fill="#555">
        {track["artist"][:25]}{"..." if len(track["artist"]) > 25 else ""}
    </text>
    <text x="120" y="90" font-family="Arial" font-size="14" fill="#777">
        {"▶ Сейчас играет" if track["now_playing"] else "⏱ " + datetime.now().strftime("%H:%M")}
    </text>
</svg>'''

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    track = get_track_info()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(create_svg(track))

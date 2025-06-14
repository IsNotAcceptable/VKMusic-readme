import os
import requests
from datetime import datetime

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = "assets/lastfm_widget.svg"

def get_track_info():
    """Получаем данные трека с улучшенной обработкой ошибок"""
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
            "now_playing": track.get("@attr", {}).get("nowplaying", "false") == "true"
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    
    return None

def create_svg(track_data):
    """Генерируем SVG с улучшенной оболочкой"""
    track = track_data or {
        "name": "Нет данных о треке",
        "artist": "Проверьте настройки Last.fm",
        "now_playing": False
    }
    
    return f'''<svg width="350" height="120" xmlns="http://www.w3.org/2000/svg">
    <!-- Внешняя оболочка с тенью -->
    <rect width="100%" height="100%" rx="10" fill="#1A1A1A"/>
    
    <!-- Внутренняя рамка -->
    <rect x="5" y="5" width="340" height="110" rx="8" fill="#9400D3" stroke="#EEE" stroke-width="2"/>
    
    <!-- Заголовок -->
    <text x="20" y="30" font-family="Arial" font-size="14" fill="#EEE" font-weight="bold">
        Сейчас слушаю (Last.fm)
    </text>
    
    <!-- Разделительная линия -->
    <line x1="20" y1="40" x2="330" y2="40" stroke="#EEE" stroke-width="1" stroke-dasharray="5,3"/>
    
    <!-- Информация о треке -->
    <text x="20" y="65" font-family="Arial" font-size="16" fill="white">
        {track["name"][:25]}{"..." if len(track["name"]) > 25 else ""}
    </text>
    <text x="20" y="90" font-family="Arial" font-size="14" fill="#EEE">
        {track["artist"][:25]}{"..." if len(track["artist"]) > 25 else ""}
    </text>
    
    <!-- Статус -->
    <text x="20" y="115" font-family="Arial" font-size="12" fill="#DDD">
        {"▶ Сейчас играет" if track["now_playing"] else "⏱ " + datetime.now().strftime("%H:%M")}
    </text>
</svg>'''

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    track = get_track_info()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(create_svg(track))

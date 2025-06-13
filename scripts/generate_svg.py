import os
import requests
from datetime import datetime

# Конфигурация
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '../assets/lastfm_widget.svg')

def get_track_info():
    """Получаем данные о текущем треке"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        track = data["recenttracks"]["track"][0]
        is_now_playing = track.get("@attr", {}).get("nowplaying", False)
        
        return {
            "track": track["name"][:30] + ("..." if len(track["name"]) > 30 else ""),
            "artist": track["artist"]["#text"][:30] + ("..." if len(track["artist"]["#text"]) > 30 else ""),
            "status": "Сейчас играет" if is_now_playing else f"Обновлено: {datetime.now().strftime('%H:%M')}",
            "image": track.get("image", [{}])[-1].get("#text", "")
        }
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None

def generate_svg(track_data):
    """Генерируем корректный SVG"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="350" height="100" viewBox="0 0 350 100" xmlns="http://www.w3.org/2000/svg">
    <style>
        .background {{ fill: #1DB954; border-radius: 5px; }}
        .text {{ font-family: Arial, sans-serif; fill: white; }}
        .track {{ font-size: 16px; font-weight: bold; }}
        .artist {{ font-size: 14px; }}
        .status {{ font-size: 12px; }}
    </style>
    
    <rect width="100%" height="100%" class="background" rx="5"/>
    
    <text x="20" y="30" class="text track">{track_data["track"]}</text>
    <text x="20" y="50" class="text artist">{track_data["artist"]}</text>
    <text x="20" y="80" class="text status">{track_data["status"]}</text>
</svg>'''

if __name__ == "__main__":
    # Создаем папку assets, если её нет
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    track = get_track_info()
    if track:
        svg_content = generate_svg(track)
        try:
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                f.write(svg_content)
            print("SVG успешно сгенерирован")
        except Exception as e:
            print(f"Ошибка при сохранении SVG: {e}")
    else:
        # Создаем пустой SVG при ошибке
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write('''<?xml version="1.0"?>
<svg width="350" height="100" xmlns="http://www.w3.org/2000/svg">
    <text x="20" y="50" font-family="Arial">Ошибка загрузки данных</text>
</svg>''')

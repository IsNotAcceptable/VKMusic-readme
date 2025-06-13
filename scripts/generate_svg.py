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
        data = response.json()
        track = data["recenttracks"]["track"][0]
        
        # Получаем обложку (последний доступный размер)
        cover_url = track.get("image", [{}])[-1].get("#text", None)
        
        return {
            "name": track.get("name", "Неизвестный трек"),
            "artist": track["artist"].get("#text", "Неизвестный исполнитель"),
            "now_playing": track.get("@attr", {}).get("nowplaying", "false") == "true",
            "cover": cover_url if cover_url and not "placeholder" in cover_url.lower() else None
        }
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def create_svg(track_data):
    """Генерируем SVG с обложкой"""
    track = track_data or {
        "name": "Нет данных",
        "artist": "Проверьте настройки",
        "now_playing": False,
        "cover": None
    }
    
    # Основной SVG-шаблон
    svg_template = '''<svg width="400" height="150" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <defs>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="2" dy="2" stdDeviation="2" flood-color="#00000080"/>
        </filter>
    </defs>
    
    <rect width="100%" height="100%" fill="#9400D3" rx="6"/>'''
    
    # Добавляем обложку или заглушку
    if track["cover"]:
        svg_template += f'''
    <image href="{track["cover"]}" x="20" y="20" width="110" height="110" filter="url(#shadow)" preserveAspectRatio="xMidYMid meet"/>'''
    else:
        svg_template += '''
    <rect x="20" y="20" width="110" height="110" fill="#6A0099" rx="4"/>
    <text x="75" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="white">No cover</text>'''
    
    # Добавляем текст
    svg_template += f'''
    <text x="150" y="40" font-family="Arial" font-size="16" font-weight="bold" fill="white">
        {track["name"][:20]}{"..." if len(track["name"]) > 20 else ""}
    </text>
    <text x="150" y="70" font-family="Arial" font-size="14" fill="#EEE">
        {track["artist"][:20]}{"..." if len(track["artist"]) > 20 else ""}
    </text>
    <text x="150" y="100" font-family="Arial" font-size="12" fill="#DDD">
        {"▶ Сейчас играет" if track["now_playing"] else "⏱ " + datetime.now().strftime("%H:%M")}
    </text>
</svg>'''
    
    return svg_template

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    track = get_track_info()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(create_svg(track))

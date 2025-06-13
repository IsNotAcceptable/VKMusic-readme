import os
import requests
from datetime import datetime
from urllib.parse import quote

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = "assets/lastfm_widget.svg"

def get_track_info():
    """Получаем данные трека с обложкой"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    try:
        print("⌛ Запрос данных из Last.fm...")
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data.get("recenttracks", {}).get("track"):
            return None
            
        track = data["recenttracks"]["track"][0]
        print(f"🎵 Получен трек: {track.get('name')} - {track['artist']['#text']}")
        
        # Получаем обложку максимального размера
        cover_url = None
        if track.get("image"):
            # Ищем в порядке убывания размера
            for size in ["extralarge", "large", "medium", "small"]:
                for img in track["image"]:
                    if img.get("size") == size and img.get("#text"):
                        cover_url = img["#text"]
                        break
                if cover_url:
                    break
        
        print(f"🖼️ Обложка: {cover_url if cover_url else 'не найдена'}")
        return {
            "name": track.get("name", "Неизвестный трек"),
            "artist": track["artist"].get("#text", "Неизвестный исполнитель"),
            "now_playing": track.get("@attr", {}).get("nowplaying", "false") == "true",
            "cover": quote(cover_url, safe=":/") if cover_url else None  # Кодируем URL
        }
        
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return None

def create_svg(track_data):
    """Генерируем SVG с обложкой"""
    track = track_data or {
        "name": "Нет данных",
        "artist": "Проверьте настройки",
        "now_playing": False,
        "cover": None
    }
    
    # Блок обложки
    cover_block = ''
    if track["cover"]:
        cover_block = f'''
    <defs>
        <clipPath id="coverClip">
            <rect x="20" y="20" width="110" height="110" rx="8"/>
        </clipPath>
    </defs>
    <image href="{track['cover']}" x="20" y="20" width="110" height="110" 
           clip-path="url(#coverClip)" preserveAspectRatio="xMidYMid cover"/>'''
    else:
        cover_block = '''
    <rect x="20" y="20" width="110" height="110" fill="#6A0099" rx="8"/>
    <text x="75" y="70" text-anchor="middle" font-family="Arial" font-size="12" fill="white">No cover</text>'''
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="450" height="150" viewBox="0 0 450 150" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect width="100%" height="100%" fill="#9400D3" rx="8"/>
    {cover_block}
    <text x="150" y="40" font-family="Arial" font-size="18" font-weight="bold" fill="white">
        {track["name"][:20]}{"..." if len(track["name"]) > 20 else ""}
    </text>
    <text x="150" y="70" font-family="Arial" font-size="16" fill="#EEE">
        {track["artist"][:20]}{"..." if len(track["artist"]) > 20 else ""}
    </text>
    <text x="150" y="100" font-family="Arial" font-size="14" fill="#DDD">
        {"▶ Сейчас играет" if track["now_playing"] else "⏱ " + datetime.now().strftime("%H:%M")}
    </text>
</svg>'''

if __name__ == "__main__":
    print("\n=== 🎶 Генерация виджета ===")
    os.makedirs("assets", exist_ok=True)
    
    track = get_track_info()
    svg_content = create_svg(track)
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("✅ Виджет успешно сгенерирован")

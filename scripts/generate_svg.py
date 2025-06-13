import os
import requests
from datetime import datetime
from urllib.parse import quote
import base64

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = "assets/lastfm_widget.svg"

def download_image(url):
    """Загружаем обложку и конвертируем в base64"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"data:image/jpeg;base64,{base64.b64encode(response.content).decode('utf-8')}"
    except Exception:
        return None

def get_track_info():
    """Получаем данные трека с обложкой"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        track = data["recenttracks"]["track"][0]
        
        # Получаем URL обложки максимального размера
        cover_url = next(
            (img["#text"] for img in reversed(track["image"]) 
            if img.get("#text") and not "placeholder" in img["#text"].lower()
        , None)
        
        # Загружаем и конвертируем обложку
        cover_data = download_image(cover_url) if cover_url else None
        
        return {
            "name": track.get("name", "Неизвестный трек"),
            "artist": track["artist"].get("#text", "Неизвестный исполнитель"),
            "now_playing": track.get("@attr", {}).get("nowplaying", False),
            "cover": cover_data
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_svg(track):
    """Генерируем SVG с встроенной обложкой"""
    svg_content = f'''<svg width="450" height="150" xmlns="http://www.w3.org/2000/svg">
    <style>
        .background {{ fill: #9400D3; rx: 8px; }}
        .text {{ font-family: Arial, sans-serif; fill: white; }}
        .cover {{ clip-path: url(#coverClip); }}
    </style>
    
    <defs>
        <clipPath id="coverClip">
            <rect x="20" y="20" width="110" height="110" rx="8"/>
        </clipPath>
    </defs>
    
    <rect width="100%" height="100%" class="background" rx="8"/>'''
    
    if track["cover"]:
        svg_content += f'''
    <image href="{track['cover']}" x="20" y="20" width="110" height="110" class="cover"/>'''
    else:
        svg_content += '''
    <rect x="20" y="20" width="110" height="110" fill="#6A0099" rx="8"/>
    <text x="75" y="65" text-anchor="middle" font-size="12" fill="white">No cover</text>'''
    
    svg_content += f'''
    <text x="150" y="40" font-size="18" font-weight="bold">{track["name"][:20]}{"..." if len(track["name"]) > 20 else ""}</text>
    <text x="150" y="70" font-size="16" fill="#EEE">{track["artist"][:20]}{"..." if len(track["artist"]) > 20 else ""}</text>
    <text x="150" y="100" font-size="14" fill="#DDD">
        {"▶ Сейчас играет" if track["now_playing"] else "⏱ " + datetime.now().strftime("%H:%M")}
    </text>
</svg>'''
    
    return svg_content

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

import os
import requests
from datetime import datetime
from urllib.parse import quote

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")
OUTPUT_PATH = "assets/lastfm_widget.svg"

def debug_log(message):
    """Логирование для отладки"""
    with open("debug.log", "a") as f:
        f.write(f"{datetime.now()}: {message}\n")

def get_track_info():
    """Получаем данные трека с обложкой"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1&extended=1"
    
    try:
        debug_log("Запрос к Last.fm API")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        debug_log(f"Ответ API: {data}")
        
        if not data.get("recenttracks", {}).get("track"):
            debug_log("Нет данных о треках")
            return None
            
        track = data["recenttracks"]["track"][0]
        debug_log(f"Данные трека: {track}")
        
        # Получаем обложку максимального размера
        cover_url = None
        if track.get("image"):
            for img in track["image"]:
                if img.get("size") == "extralarge":
                    cover_url = img.get("#text")
                    break
            if not cover_url and track["image"]:
                cover_url = track["image"][-1].get("#text")
        
        debug_log(f"URL обложки: {cover_url}")
        
        return {
            "name": track.get("name", "Неизвестный трек"),
            "artist": track["artist"].get("#text", "Неизвестный исполнитель"),
            "now_playing": track.get("@attr", {}).get("nowplaying", "false") == "true",
            "cover": cover_url
        }
        
    except Exception as e:
        debug_log(f"Ошибка: {str(e)}")
        return None

def create_svg(track_data):
    """Генерируем SVG с обложкой"""
    track = track_data or {
        "name": "Нет данных о треке",
        "artist": "Проверьте настройки",
        "now_playing": False,
        "cover": None
    }
    
    svg_content = f'''<svg width="450" height="150" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <defs>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="2" dy="2" stdDeviation="2" flood-color="#00000080"/>
        </filter>
    </defs>
    
    <rect width="100%" height="100%" fill="#9400D3" rx="6"/>'''
    
    # Блок обложки
    if track["cover"] and not "placeholder" in track["cover"].lower():
        svg_content += f'''
    <image href="{track["cover"]}" x="20" y="20" width="110" height="110" filter="url(#shadow)" preserveAspectRatio="xMidYMid meet"/>'''
        debug_log("Добавлена обложка в SVG")
    else:
        svg_content += '''
    <rect x="20" y="20" width="110" height="110" fill="#6A0099" rx="4"/>
    <text x="75" y="70" text-anchor="middle" font-family="Arial" font-size="12" fill="white">No cover</text>'''
        debug_log("Использована заглушка обложки")
    
    # Блок текста
    svg_content += f'''
    <text x="150" y="40" font-family="Arial" font-size="18" font-weight="bold" fill="white">
        {track["name"][:20]}{"..." if len(track["name"]) > 20 else ""}
    </text>
    <text x="150" y="70" font-family="Arial" font-size="16" fill="#EEE">
        {track["artist"][:20]}{"..." if len(track["artist"]) > 20 else ""}
    </text>
    <text x="150" y

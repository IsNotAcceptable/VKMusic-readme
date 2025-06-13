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
        print("⌛ Запрос данных из Last.fm...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("recenttracks", {}).get("track"):
            print("⚠️ Last.fm не вернул данные о треках")
            return None
            
        track = data["recenttracks"]["track"][0]
        print(f"🎵 Получен трек: {track.get('name', 'Без названия')} - {track['artist'].get('#text', 'Неизвестный исполнитель')}")
        
        # Получаем обложку (берем последний доступный размер)
        cover_url = track.get("image", [{}])[-1].get("#text")
        if cover_url and "placeholder" not in cover_url.lower():
            print(f"🖼️ Обложка: {cover_url}")
        else:
            print("🖼️ Обложка не найдена")
            cover_url = None
            
        return {
            "name": track.get("name", "Неизвестный трек"),
            "artist": track["artist"].get("#text", "Неизвестный исполнитель"),
            "now_playing": track.get("@attr", {}).get("nowplaying", "false") == "true",
            "cover": cover_url
        }
        
    except requests.exceptions.RequestException as e:
        print(f"🚨 Ошибка запроса: {e}")
    except Exception as e:
        print(f"⚠️ Неожиданная ошибка: {e}")
    
    return None

def create_svg(track_data):
    """Генерируем SVG с проверкой обложки"""
    track = track_data or {
        "name": "Нет данных",
        "artist": "Проверьте настройки",
        "now_playing": False,
        "cover": None
    }
    
    # Блок обложки
    cover_block = ""
    if track["cover"]:
        cover_block = f'<image href="{track["cover"]}" x="20" y="20" width="110" height="110" preserveAspectRatio="xMidYMid meet"/>'
        print("✅ Добавлена обложка в SVG")
    else:
        cover_block = '''
        <rect x="20" y="20" width="110" height="110" fill="#6A0099" rx="4"/>
        <text x="75" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="white">No cover</text>'''
        print("ℹ️ Использована заглушка обложки")
    
    return f'''<svg width="400" height="150" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect width="100%" height="100%" fill="#9400D3" rx="6"/>
    {cover_block}
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

if __name__ == "__main__":
    print("\n=== 🎶 Генерация Last.fm виджета ===")
    os.makedirs("assets", exist_ok=True)
    
    track = get_track_info()
    svg_content = create_svg(track)
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("✅ SVG успешно сгенерирован\n")

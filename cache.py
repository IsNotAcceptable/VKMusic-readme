import json
import os
from datetime import datetime

CACHE_FILE = 'last_track.json'

def save_last_track(artist, title, cover_url):
    """Сохраняет последний проигранный трек"""
    data = {
        'artist': artist,
        'title': title,
        'cover_url': cover_url,
        'timestamp': datetime.now().isoformat()
    }
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_last_track():
    """Получает последний сохранённый трек"""
    if not os.path.exists(CACHE_FILE):
        return None, None, None
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('artist'), data.get('title'), data.get('cover_url')
    except:
        return None, None, None

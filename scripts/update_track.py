import os
import requests
import re

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")

def get_current_track():
    """Получает текущий или последний трек из Last.fm"""
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    response = requests.get(url)
    data = response.json()
    
    track = data["recenttracks"]["track"][0]
    is_now_playing = "@attr" in track and "nowplaying" in track["@attr"]
    
    return {
        "name": track["name"],
        "artist": track["artist"]["#text"],
        "is_now_playing": is_now_playing
    }

def update_readme(track):
    """Обновляет README.md с новым треком"""
    with open("../README.md", "r") as f:
        readme = f.read()

    status = "Сейчас играет" if track["is_now_playing"] else "Последний трек"
    track_text = f"🎵 **{status}**: {track['name']} — {track['artist']}"

    new_readme = re.sub(
        r"<!-- LASTFM_START -->.*<!-- LASTFM_END -->",
        f"<!-- LASTFM_START -->{track_text}<!-- LASTFM_END -->",
        readme,
        flags=re.DOTALL
    )
    
    with open("../README.md", "w") as f:
        f.write(new_readme)

if __name__ == "__main__":
    track = get_current_track()
    update_readme(track)

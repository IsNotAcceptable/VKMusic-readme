import os
import requests


def get_cover_url(artist, title):
    try:
        r = requests.get('https://ws.audioscrobbler.com/2.0/', params={
            'method': 'track.getInfo',
            'api_key': os.environ['LASTFM_API_KEY'],
            'artist': artist,
            'track': title,
            'format': 'json'
        }).json()

        images = r.get('track', {}).get('album', {}).get('image', [])
        for img in reversed(images):
            url = img.get('#text', '')
            if url:
                return url

    except Exception as e:
        print(f"Last.fm exception: {e}")

    return None

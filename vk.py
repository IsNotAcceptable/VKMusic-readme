import os
import requests


def get_vk_music():
    try:
        r = requests.get('https://api.vk.com/method/status.get', params={
            'access_token': os.environ['VK_TOKEN'],
            'v': '5.131'
        }).json()

        if 'error' in r:
            print(f"VK error: {r['error']}")
            return None, None

        text = r.get('response', {}).get('text', '')
        if '—' in text:
            parts = text.split('—', 1)
            return parts[0].strip(), parts[1].strip()

        return None, None

    except Exception as e:
        print(f"VK exception: {e}")
        return None, None

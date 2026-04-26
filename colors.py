import requests
import base64
from colorthief import ColorThief
from io import BytesIO

FALLBACK_COLORS = [(30, 10, 60), (60, 20, 100)]


def get_dominant_colors(image_url):
    try:
        resp = requests.get(image_url, timeout=10)
        ct = ColorThief(BytesIO(resp.content))
        return ct.get_palette(color_count=3, quality=1)
    except Exception as e:
        print(f"ColorThief exception: {e}")
        return FALLBACK_COLORS


def image_to_base64(image_url):
    try:
        resp = requests.get(image_url, timeout=10)
        b64 = base64.b64encode(resp.content).decode('utf-8')
        content_type = resp.headers.get('Content-Type', 'image/jpeg')
        return f"data:{content_type};base64,{b64}"
    except Exception as e:
        print(f"Base64 exception: {e}")
        return None


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def darken(rgb, factor=0.35):
    return tuple(int(c * factor) for c in rgb)

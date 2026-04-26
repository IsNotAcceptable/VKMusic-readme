from colors import get_dominant_colors, image_to_base64, rgb_to_hex, darken, FALLBACK_COLORS


def truncate(text, max_chars):
    return text if len(text) <= max_chars else text[:max_chars - 1] + '…'


def generate_svg(artist, title, cover_url):
    colors = get_dominant_colors(cover_url) if cover_url else FALLBACK_COLORS

    c1 = darken(colors[0], 0.35)
    c2 = darken(colors[1] if len(colors) > 1 else colors[0], 0.25)
    c_accent = colors[0]

    hex1 = rgb_to_hex(c1)
    hex2 = rgb_to_hex(c2)
    hex_accent = rgb_to_hex(c_accent)

    cover_b64 = image_to_base64(cover_url) if cover_url else None

    if cover_b64:
        cover_block = f'<image href="{cover_b64}" x="12" y="12" width="96" height="96" clip-path="url(#cover-clip)" preserveAspectRatio="xMidYMid slice"/>'
    else:
        cover_block = f'<rect x="12" y="12" width="96" height="96" rx="8" fill="{hex_accent}" opacity="0.5"/><text x="60" y="66" text-anchor="middle" font-size="36" font-family="Arial">♫</text>'

    title_safe = truncate(title, 28) if title else 'Ничего не играет'
    artist_safe = truncate(artist, 32) if artist else ''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="480" height="120">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{hex1}"/>
      <stop offset="100%" stop-color="{hex2}"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{hex_accent}" stop-opacity="0.45"/>
      <stop offset="60%" stop-color="{hex_accent}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="cover-clip">
      <rect x="12" y="12" width="96" height="96" rx="8"/>
    </clipPath>
    <clipPath id="card-clip">
      <rect width="480" height="120" rx="16"/>
    </clipPath>
    <clipPath id="wave-clip">
      <rect x="350" y="0" width="118" height="120" rx="0"/>
    </clipPath>
    <style>
      @keyframes wave1 {{ 0% {{ d: path("M350,90 C370,75 390,105 410,90 C430,75 450,105 468,90 L468,120 L350,120 Z"); }} 50% {{ d: path("M350,90 C370,105 390,75 410,90 C430,105 450,75 468,90 L468,120 L350,120 Z"); }} 100% {{ d: path("M350,90 C370,75 390,105 410,90 C430,75 450,105 468,90 L468,120 L350,120 Z"); }} }}
      @keyframes wave2 {{ 0% {{ d: path("M350,95 C365,82 385,108 410,95 C435,82 455,108 468,95 L468,120 L350,120 Z"); }} 50% {{ d: path("M350,95 C365,108 385,82 410,95 C435,108 455,82 468,95 L468,120 L350,120 Z"); }} 100% {{ d: path("M350,95 C365,82 385,108 410,95 C435,82 455,108 468,95 L468,120 L350,120 Z"); }} }}
      @keyframes wave3 {{ 0% {{ d: path("M350,100 C370,90 395,110 420,100 C445,90 458,108 468,100 L468,120 L350,120 Z"); }} 50% {{ d: path("M350,100 C370,110 395,90 420,100 C445,110 458,92 468,100 L468,120 L350,120 Z"); }} 100% {{ d: path("M350,100 C370,90 395,110 420,100 C445,90 458,108 468,100 L468,120 L350,120 Z"); }} }}
      .w1 {{ animation: wave1 3s ease-in-out infinite; }}
      .w2 {{ animation: wave2 2.5s ease-in-out infinite .4s; }}
      .w3 {{ animation: wave3 2s ease-in-out infinite .8s; }}
    </style>
  </defs>

  <rect width="480" height="120" rx="16" fill="url(#bg)"/>
  <rect width="480" height="120" rx="16" fill="url(#fade)" clip-path="url(#card-clip)"/>

  {cover_block}
  <rect x="12" y="12" width="96" height="96" rx="8" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>

  <text x="124" y="36" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.45)" font-weight="600" letter-spacing="1.5">СЕЙЧАС ИГРАЕТ</text>
  <text x="124" y="60" font-family="Arial,sans-serif" font-size="17" fill="white" font-weight="700">{title_safe}</text>
  <text x="124" y="80" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">{artist_safe}</text>

  <rect x="124" y="96" width="220" height="3" rx="2" fill="rgba(255,255,255,0.1)"/>
  <rect x="124" y="96" width="90" height="3" rx="2" fill="{hex_accent}" opacity="0.8"/>

  <g clip-path="url(#wave-clip)">
    <path class="w1" fill="rgba(255,255,255,0.07)" d="M350,90 C370,75 390,105 410,90 C430,75 450,105 468,90 L468,120 L350,120 Z"/>
    <path class="w2" fill="rgba(255,255,255,0.05)" d="M350,95 C365,82 385,108 410,95 C435,82 455,108 468,95 L468,120 L350,120 Z"/>
    <path class="w3" fill="rgba(255,255,255,0.09)" d="M350,100 C370,90 395,110 420,100 C445,90 458,108 468,100 L468,120 L350,120 Z"/>
  </g>
</svg>'''

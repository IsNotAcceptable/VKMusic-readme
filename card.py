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
    <style>
      @keyframes wm   {{ 0%{{transform:translateX(0)}}   100%{{transform:translateX(-50%)}} }}
      @keyframes wm2  {{ 0%{{transform:translateX(0)}}   100%{{transform:translateX(50%)}}  }}
      @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.5}} }}
      .wa {{ animation: wm  6s linear infinite; }}
      .wb {{ animation: wm2 9s linear infinite; }}
      .ring {{ animation: pulse 2s ease-in-out infinite; }}
    </style>
  </defs>

  <rect width="480" height="120" rx="16" fill="url(#bg)"/>
  <rect width="480" height="120" rx="16" fill="url(#fade)" clip-path="url(#card-clip)"/>

  <g clip-path="url(#card-clip)">
    <g class="wa"><path fill="rgba(255,255,255,0.06)" d="M0,95 C60,82 120,108 180,95 C240,82 300,108 360,95 C420,82 480,108 540,95 C600,82 660,108 720,95 L720,120 L0,120 Z"/></g>
    <g class="wb"><path fill="rgba(255,255,255,0.04)" d="M0,102 C80,90 160,114 240,102 C320,90 400,114 480,102 C560,90 640,114 720,102 L720,120 L0,120 Z"/></g>
  </g>

  {cover_block}
  <rect x="12" y="12" width="96" height="96" rx="8" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>

  <text x="124" y="36" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.45)" font-weight="600" letter-spacing="1.5">СЕЙЧАС ИГРАЕТ</text>
  <text x="124" y="60" font-family="Arial,sans-serif" font-size="17" fill="white" font-weight="700">{title_safe}</text>
  <text x="124" y="80" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">{artist_safe}</text>

  <rect x="124" y="96" width="220" height="3" rx="2" fill="rgba(255,255,255,0.1)"/>
  <rect x="124" y="96" width="90" height="3" rx="2" fill="{hex_accent}" opacity="0.8"/>

  <circle class="ring" cx="415" cy="60" r="28" fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
  <circle cx="415" cy="60" r="22" fill="rgba(255,255,255,0.12)"/>
  <polygon points="409,50 409,70 431,60" fill="white" opacity="0.9"/>
</svg>'''

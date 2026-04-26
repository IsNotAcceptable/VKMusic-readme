from vk import get_vk_music
from lastfm import get_cover_url
from card import generate_svg
from readme import update_readme

if __name__ == '__main__':
    artist, title = get_vk_music()
    print(f'Трек: {artist} — {title}')

    cover_url = None
    if artist and title:
        cover_url = get_cover_url(artist, title)
        print(f'Обложка: {cover_url}')

    svg = generate_svg(artist, title, cover_url)

    with open('music-card.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('SVG сохранён')

    update_readme('./music-card.svg')

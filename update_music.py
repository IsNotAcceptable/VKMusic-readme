from vk import get_vk_music
from lastfm import get_cover_url
from card import generate_svg
from readme import update_readme
from cache import get_last_track, save_last_track

if __name__ == '__main__':
    artist, title = get_vk_music()
    print(f'Трек: {artist} — {title}')
    
    is_now_playing = bool(artist and title)
    
    # Если музыка не играет, берём последний трек из кеша
    if not is_now_playing:
        artist, title, _ = get_last_track()
        print(f'Используем последний трек: {artist} — {title}')
    
    cover_url = None
    if artist and title:
        cover_url = get_cover_url(artist, title)
        print(f'Обложка: {cover_url}')
        # Сохраняем только если получили текущий трек
        if is_now_playing:
            save_last_track(artist, title, cover_url)

    svg = generate_svg(artist, title, cover_url, is_now_playing=is_now_playing)

    with open('music-card.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('SVG сохранён')

    update_readme('./music-card.svg')

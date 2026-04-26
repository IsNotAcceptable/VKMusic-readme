def update_readme(svg_path='./music-card.svg'):
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    start_tag = '<!-- vkmusic-start -->'
    end_tag = '<!-- vkmusic-end -->'
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)

    if start_idx == -1 or end_idx == -1:
        print('Теги не найдены в README.md!')
        return

    badge = f'![Now Playing]({svg_path})'
    new_content = (
        content[:start_idx + len(start_tag)]
        + f'\n\n{badge}\n\n'
        + content[end_idx:]
    )

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('README обновлён')

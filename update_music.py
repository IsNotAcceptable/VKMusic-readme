import os
import requests

TOKEN = os.environ['VK_TOKEN']

def get_vk_status():
    try:
        url = f"https://vk.com{TOKEN}&v=5.131"
        data = requests.get(url).json()
        
        if 'response' in data:
            status = data['response'].get('text', '')
            if status:
                return f"Сейчас слушает: **{status}**"
        return "Сейчас ничего не играет"
    except Exception as e:
        return "Ошибка получения музыки"

def update_readme(new_status):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- vkmusic-start -->"
    end_tag = "<!-- vkmusic-end -->"
    
    start_idx = content.find(start_tag) + len(start_tag)
    end_idx = content.find(end_tag)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + f"\n\n{new_status}\n\n" + content[end_idx:]
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)

if __name__ == "__main__":
    status = get_vk_status()
    update_readme(status)

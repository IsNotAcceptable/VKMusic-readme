import os
import requests

TOKEN = os.environ['VK_TOKEN']

def get_vk_music():
    try:
        url = "https://api.vk.com/method/status.get"
        params = {"access_token": TOKEN, "v": "5.131"}
        data = requests.get(url, params=params).json()

        if "error" in data:
            print(f"VK Error: {data['error']}")
            return "Сейчас ничего не играет"

        text = data.get("response", {}).get("text", "")
        print(f"Status text: '{text}'")

        if text:
            return f"🎵 {text}"
        return "Сейчас ничего не играет"

    except Exception as e:
        print(f"Exception: {e}")
        return "Ошибка"

def update_readme(new_status):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- vkmusic-start -->"
    end_tag = "<!-- vkmusic-end -->"

    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)

    if start_idx == -1 or end_idx == -1:
        print("Теги не найдены в README.md!")
        return

    new_content = (
        content[:start_idx + len(start_tag)]
        + f"\n\n{new_status}\n\n"
        + content[end_idx:]
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"README обновлён: {new_status}")

if __name__ == "__main__":
    status = get_vk_music()
    update_readme(status)

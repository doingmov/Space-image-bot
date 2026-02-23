import os
from urllib.parse import unquote, urlsplit
import requests

def download_image(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    with open(path, "wb") as file:
        file.write(response.content)

    print(f"Сохранено: {path}")


def get_file_extension(url):
    path = urlsplit(url).path
    filename = os.path.split(unquote(path))[1]
    _, ext = os.path.splitext(filename)
    return ext or ".jpg"

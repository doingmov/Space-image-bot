import os
from urllib.parse import unquote, urlsplit
import requests


def download_image(url, path, params=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    with open(path, "wb") as file:
        file.write(response.content)

    print(f"Сохранено: {path}")


def get_file_extension(url):
    path = urlsplit(url).path
    filename = os.path.basename(unquote(path))
    _, ext = os.path.splitext(filename)
    return ext or ".jpg"

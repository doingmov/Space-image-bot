import os
import requests
from utils import download_image, get_file_extension


def fetch_nasa_apod_images(api_key, count=30, output_dir="nasa_images"):
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": count}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    for i, item in enumerate(data, start=1):
        if item.get("media_type") != "image":
            continue

        img_url = item.get("url")
        ext = get_file_extension(img_url)
        file_path = os.path.join(output_dir, f"apod{i}{ext}")

        try:
            download_image(img_url, file_path)
        except requests.RequestException as e:
            print(f"Не удалось скачать {img_url}: {e}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    import argparse

    load_dotenv()

    parser = argparse.ArgumentParser(description="Скачивает изображения NASA APOD")
    parser.add_argument(
        "--count",
        type=int,
        default=30,
        help="Количество изображений для скачивания"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getenv("NASA_APOD_DIR", "nasa_images"),
        help="Папка для сохранения изображений (можно задать через переменную окружения NASA_APOD_DIR)"
    )
    parser.add_argument(
        "--api_key",
        type=str,
        default=os.getenv("NASA_API_KEY"),
        help="Ключ API NASA (можно задать через переменную окружения NASA_API_KEY)"
    )
    args = parser.parse_args()

    fetch_nasa_apod_images(api_key=args.api_key, count=args.count, output_dir=args.dir)

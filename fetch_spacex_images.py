import os
import requests
import argparse
from utils import download_image

def fetch_spacex_images(count=10, launch_id="latest", output_dir="spacex_images"):
    url = f"https://api.spacexdata.com/v4/launches/{launch_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    images = data.get("links", {}).get("flickr", {}).get("original", [])[:count]

    if not images:
        print("Нет доступных изображений SpaceX")
        return

    os.makedirs(output_dir, exist_ok=True)

    for i, img_url in enumerate(images, start=1):
        file_path = os.path.join(output_dir, f"launch{i}.jpg")
        try:
            download_image(img_url, file_path)
        except requests.RequestException as e:
            print(f"Не удалось скачать {img_url}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивает изображения запуска SpaceX")
    parser.add_argument(
        "--launch_id",
        type=str,
        default="latest",
        help="ID запуска SpaceX для скачивания изображений или 'latest' (по умолчанию)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Количество изображений для скачивания"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getenv("SPACEX_IMAGES_DIR", "spacex_images"),
        help="Папка для сохранения изображений SpaceX (можно задать через переменную окружения SPACEX_IMAGES_DIR)"
    )
    args = parser.parse_args()

    fetch_spacex_images(count=args.count, launch_id=args.launch_id, output_dir=args.dir)

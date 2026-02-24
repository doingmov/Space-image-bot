import os
import requests
from datetime import datetime
from utils import download_image


def fetch_epic_images(api_key, count=10, output_dir="epic_images"):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    if not data:
        print("Нет доступных изображений EPIC")
        return

    for i, item in enumerate(data[:count], start=1):
        if "image" not in item or "date" not in item:
            continue

        image_name = item["image"]
        date = datetime.strptime(item["date"].split()[0], "%Y-%m-%d")
        year, month, day = date.strftime("%Y/%m/%d").split("/")

        base_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
        )

        file_path = os.path.join(output_dir, f"epic{i}.png")

        try:
            download_image(base_url, file_path, params={"api_key": api_key})
        except requests.RequestException as e:
            print(f"Не удалось скачать {base_url}: {e}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    import argparse

    load_dotenv()

    parser = argparse.ArgumentParser(description="Скачивает изображения NASA EPIC")
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Количество изображений для скачивания"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getenv("NASA_EPIC_DIR", "epic_images"),
        help="Папка для сохранения изображений (можно задать через переменную окружения NASA_EPIC_DIR)"
    )
    parser.add_argument(
        "--api_key",
        type=str,
        default=os.getenv("NASA_API_KEY"),
        help="Ключ API NASA (можно задать через переменную окружения NASA_API_KEY)"
    )
    args = parser.parse_args()

    fetch_epic_images(api_key=args.api_key, count=args.count, output_dir=args.dir)

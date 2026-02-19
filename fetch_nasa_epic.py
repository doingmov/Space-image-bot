import requests
import os
from datetime import datetime
from utils import download_image
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")


def fetch_epic_images(count=10):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": NASA_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        print("Ошибка с вашим ключом, пробуем DEMO_KEY")
        params["api_key"] = "DEMO_KEY"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            print("Сервис NASA EPIC временно недоступен.")
            return

    data = response.json()
    if not data:
        print("Нет доступных изображений EPIC")
        return

    os.makedirs("epic_images", exist_ok=True)

    for i, item in enumerate(data[:count], start=1):
        if "image" not in item or "date" not in item:
            continue
        image_name = item["image"]
        date = datetime.strptime(item["date"].split()[0], "%Y-%m-%d")
        year, month, day = date.strftime("%Y/%m/%d").split("/")
        img_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={params['api_key']}"
        file_path = f"epic_images/epic{i}.png"
        download_image(img_url, file_path)


if __name__ == "__main__":
    fetch_epic_images(count=10)


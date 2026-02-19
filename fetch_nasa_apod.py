import requests
import os
from utils import download_image, get_file_extension
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")


def fetch_nasa_apod_images(count=30):
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY, "count": count}
    
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
            print("Сервис NASA APOD временно недоступен.")
            return
    
    data = response.json()
    os.makedirs("nasa_images", exist_ok=True)
    
    for i, item in enumerate(data, start=1):
        if item.get("media_type") != "image":
            continue
        img_url = item.get("url")
        ext = get_file_extension(img_url)
        file_path = f"nasa_images/apod{i}{ext}"
        download_image(img_url, file_path)


if __name__ == "__main__":
    fetch_nasa_apod_images(count=30)

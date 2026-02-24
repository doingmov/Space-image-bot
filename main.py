import os
import requests
from dotenv import load_dotenv

from fetch_spacex_images import fetch_spacex_images
from fetch_nasa_apod import fetch_nasa_apod_images
from fetch_nasa_epic import fetch_epic_images


def main():
    load_dotenv()

    nasa_api_key = os.getenv("NASA_API_KEY")
    if not nasa_api_key:
        raise ValueError(
            "Не указан токен NASA_API_KEY. "
            "Получите токен на https://api.nasa.gov"
        )

    try:
        fetch_spacex_images(count=5)
    except requests.RequestException as e:
        print(f"Не удалось загрузить изображения SpaceX: {e}")

    try:
        fetch_nasa_apod_images(api_key=nasa_api_key, count=10)
    except requests.HTTPError as e:
        print(f"Ошибка при загрузке APOD изображений: {e}")

    try:
        fetch_epic_images(api_key=nasa_api_key, count=5)
    except requests.HTTPError as e:
        print(f"Ошибка при загрузке EPIC изображений: {e}")


if __name__ == "__main__":
    main()

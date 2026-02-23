import os
from dotenv import load_dotenv
from fetch_spacex_images import fetch_spacex_images
from fetch_nasa_apod import fetch_nasa_apod_images
from fetch_nasa_epic import fetch_epic_images
import requests

def main():
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']

    try:
        fetch_spacex_images(count=5)
    except requests.RequestException:
        print("Не удалось загрузить изображения SpaceX")

    try:
        fetch_nasa_apod_images(api_key=nasa_api_key, count=10)
    except requests.RequestException:
        print("Ошибка при загрузке APOD изображений. Пробуем DEMO_KEY…")
        try:
            fetch_nasa_apod_images(api_key="DEMO_KEY", count=10)
        except requests.RequestException:
            print("Сервис NASA APOD временно недоступен.")

    try:
        fetch_epic_images(api_key=nasa_api_key, count=5)
    except requests.RequestException:
        print("Ошибка при загрузке EPIC изображений. Пробуем DEMO_KEY…")
        try:
            fetch_epic_images(api_key="DEMO_KEY", count=5)
        except requests.RequestException:
            print("Сервис NASA EPIC временно недоступен.")

if __name__ == "__main__":
    main()

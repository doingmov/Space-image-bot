import argparse
import requests
from utils import download_image, get_file_extension
import os


def fetch_spacex_images(launch_id=None):
    if not launch_id:
        url = "https://api.spacexdata.com/v5/launches/latest"
    else:
        url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        print("Не удалось получить данные SpaceX")
        return

    data = response.json()
    images = data["links"]["flickr"]["original"]
    os.makedirs("images", exist_ok=True)
    
    for i, img_url in enumerate(images, start=1):
        ext = get_file_extension(img_url)
        file_path = f"images/spacex{i}{ext}"
        download_image(img_url, file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch_id", type=str, help="5eb87d47ffd86e000604b38a")
    args = parser.parse_args()
    fetch_spacex_images(args.launch_id)

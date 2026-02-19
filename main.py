from fetch_spacex_images import fetch_spacex_images
from fetch_nasa_apod import fetch_nasa_apod_images
from fetch_nasa_epic import fetch_epic_images
import os
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

fetch_spacex_images()
fetch_nasa_apod_images(NASA_API_KEY, count=30)
fetch_epic_images(NASA_API_KEY, count=10)

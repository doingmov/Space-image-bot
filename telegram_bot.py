import os
import time
import random
import argparse
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

def auto_publish(bot_token, chat_id, images_dir, delay_hours=4):
    bot = Bot(token=bot_token)
    
    images = [os.path.join(images_dir, f) for f in os.listdir(images_dir)
              if os.path.isfile(os.path.join(images_dir, f))]
    
    if not images:
        print(f"Нет изображений в папке {images_dir}")
        return

    while True:
        random.shuffle(images)
        for photo_path in images:
            try:
                with open(photo_path, "rb") as photo:
                    bot.send_photo(chat_id=chat_id, photo=photo)
                print(f"Опубликовано: {photo_path}")
            except Exception as e:
                print(f"Не удалось опубликовать {photo_path}: {e}")
            
            time.sleep(delay_hours * 3600)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat_id", type=str, required=True, help="ID или @username канала")
    parser.add_argument("--dir", type=str, default="images", help="Папка с изображениями")
    parser.add_argument("--delay", type=float, default=4, help="Задержка между публикациями в часах")
    args = parser.parse_args()
    TOKEN = os.getenv("TELEGRAM_TOKEN")

    auto_publish(TOKEN, args.chat_id, args.dir, args.delay)

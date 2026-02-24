import os
import time
import random
import argparse
from telegram import Bot
from telegram.error import NetworkError, TelegramError, RetryAfter

def publish_images_periodically(bot_token, chat_id, images_dir, delay_hours=4):
    bot = Bot(token=bot_token)
    
    images = [
        os.path.join(images_dir, f)
        for f in os.listdir(images_dir)
        if os.path.isfile(os.path.join(images_dir, f))
    ]
    
    if not images:
        print(f"Нет изображений в папке {images_dir}")
        return

    while True:
        random.shuffle(images)
        for photo_path in images:
            while True:
                try:
                    with open(photo_path, "rb") as photo:
                        bot.send_photo(chat_id=chat_id, photo=photo)
                except (NetworkError, TelegramError, RetryAfter, OSError) as e:
                    print(f"Не удалось опубликовать {photo_path}: {e}. Попытка через 10 секунд...")
                    time.sleep(10)
                else:
                    print(f"Опубликовано: {photo_path}")
                    break

            time.sleep(delay_hours * 3600)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--chat_id", type=str, required=True)
    parser.add_argument("--dir", type=str, default="images")
    parser.add_argument("--delay", type=float, default=4)
    args = parser.parse_args()

    TOKEN = os.environ['TELEGRAM_TOKEN']
    publish_images_periodically(TOKEN, args.chat_id, args.dir, args.delay)

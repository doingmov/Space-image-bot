import os
import time
import random
import argparse
from telegram import Bot
import telegram.error

def publish_images_periodically(bot_token, chat_id, images_dir, delay_hours=4):
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
            except (telegram.error.TelegramError, OSError) as e:
                print(f"Не удалось опубликовать {photo_path}: {e}")
            else:
                print(f"Опубликовано: {photo_path}")
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
    auto_publish(TOKEN, args.chat_id, args.dir, args.delay)

import os
import sys
import logging
from random import randint, choice
from datetime import datetime, timedelta

import telebot
from telebot import types

from utils.pars import main_pars
from core.setting import TOKEN, PGCONNECTION


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
bot = telebot.TeleBot(TOKEN)


def create_user_tables(): 
    with PGCONNECTION.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tg_users (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                username VARCHAR(255),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        PGCONNECTION.commit()
        logger.info("User table created successfully")


def insert_user(user: types.User):
    with PGCONNECTION.cursor() as cursor:
        cursor.execute("""
            INSERT INTO tg_users (user_id, username, first_name, last_name)
            VALUES (%s, %s, %s, %s)
        """, (user.id, user.username, user.first_name, user.last_name))
        PGCONNECTION.commit()
        logger.info(f"User {user.id} inserted successfully")
        

def check_user(user: types.User):
    with PGCONNECTION.cursor() as cursor:
        cursor.execute(f"SELECT * FROM tg_users WHERE user_id = {user.id}")
        result = cursor.fetchone()
        return result if result else None


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    
    if check_user(message.from_user) is None:
        insert_user(message.from_user)

    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(content_types=['text'])
def base_currency_function(message: types.Message):
    # 56
    rate = message.text

    if not rate.isdigit():
        bot.send_message(message.chat.id, "Введите целое число")
        return

    if int(rate) <= 0:
        bot.send_message(message.chat.id, "Введите число больше нуля")
        return

    if int(rate) >= 1000000:
        bot.send_message(message.chat.id, "Введите число меньше 1 000 000")
        return

    curencies = ["kgs", "rub", "usd", "eur", "uah","azn","btc"]
    bot.reply_to(message, f" Change {rate} KZT \n Start......")

    for currency in curencies:
        try:
            bot.send_message(message.chat.id, f"{main_pars(currency, rate)}")

        except Exception as e:
            logger.error(f"Ошибка при обмене KZT на {currency}: {e}")
            continue

    
    bot.send_message(message.chat.id,"change finish")


if __name__ == "__main__":
    try:
        create_user_tables()
        logger.info("Starting the application...")
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

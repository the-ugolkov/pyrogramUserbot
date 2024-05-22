import asyncio
import os

from pyrogram import Client

from app_user.logic import get_users, update_user_status, init_db
from app_user.models import StatusEnum
from logs import setup_logger
from pyrogram_app.config import api_id
from texts import TEXTS

from dotenv import load_dotenv

load_dotenv()

info_logger = setup_logger('cycle', 'INFO')
warning_logger = setup_logger('cycle', 'WARNING')

trigger_words = os.getenv('FINISH_TRIGGERS').split(' ')
trigger = [os.getenv('TRIGGER')]
session_file = os.getenv('session_file2')


async def main_cycle():
    info_logger.info('start While')
    while True:
        for num, text in TEXTS.items():
            await check_and_send_messages(num, text)
        await asyncio.sleep(60)


async def check_and_send_messages(num, text):
    await init_db()
    user_ids = await get_users(num)

    for id in user_ids:
        try:
            check_triggers = await check_messages_for_triggers(id, trigger_words)
            if check_triggers:
                info_logger.info(f"User {id} - finished by trigger")
                await update_user_status(id, StatusEnum.finished)
                continue

            check_second = await check_messages_for_triggers(id, trigger)
            if num == 2 and check_second:
                continue

            await send_message(id, text)
        except Exception as er:
            warning_logger.warning(f"User {id} - dead ({er})")
            await update_user_status(id, StatusEnum.dead)

        if num == 3:
            info_logger.info(f"User {id} - finished by final message")
            await update_user_status(id, StatusEnum.finished)


async def send_message(user_id, text):
    async with Client(session_file, api_id) as app:
        await app.send_message(user_id, text)


async def check_messages_for_triggers(user_id, triggers):
    async with Client(session_file, api_id) as app:
        me = await app.get_me()
        async for message in app.get_chat_history(user_id):
            if (message.from_user and message.from_user.id == me.id) and any(
                    trigger_word.lower() in message.text.lower() for trigger_word in triggers):
                return message.text
            else:
                continue

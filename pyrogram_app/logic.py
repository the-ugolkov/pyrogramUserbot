import asyncio
import os

from app_user.logic import get_users, update_user_status
from app_user.models import StatusEnum
from pyrogram_app.config import app
from texts import texts

trigger_words = os.getenv('FINISH_TRIGGERS').split(' ')
trigger = [os.getenv('TRIGGER')]


async def main_cycle():
    print('start While')
    while True:
        print('start again While')
        for num, text in texts.items():
            print(f'check {num} category')
            user_ids = get_users(num)
            print(user_ids)
            for id in user_ids:
                try:
                    check_triggers = await check_messages_for_triggers(id, trigger_words)
                    check_second = await check_messages_for_triggers(id, trigger)
                    if check_triggers:
                        update_user_status(id, StatusEnum.finished)
                        continue
                    if num == 2 and check_second:
                        continue
                    await app.send_message(id, text)
                except Exception as er:
                    print(er)
                    update_user_status(id, StatusEnum.dead)
        await asyncio.sleep(60)


async def check_messages_for_triggers(user_id, triggers):
    async for message in app.get_chat_history(user_id):
        if any(trigger_word in message.text for trigger_word in triggers):
            pass
        else:
            return

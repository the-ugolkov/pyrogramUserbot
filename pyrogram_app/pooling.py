import asyncio

from pyrogram import filters

from app_user.logic import create_user
from pyrogram_app.config import app


@app.on_message(filters.private & filters.text)
def handle_message(client, message):
    print('123')
    asyncio.run(create_user(message.from_user.id))
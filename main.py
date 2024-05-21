from pyrogram import filters

from app_user.logic import create_user
from pyrogram_app.config import app


@app.on_message(filters.private & filters.text)
async def handle_message(client, message):
    print('handle_message')
    await create_user(message.from_user.id)


if __name__ == "__main__":
    app.run()

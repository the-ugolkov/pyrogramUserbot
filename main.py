from pyrogram import filters

from app_user.logic import create_user, init_db
from logs import setup_logger
from pyrogram_app.config import app

info_logger = setup_logger('handler', 'INFO')


@app.on_message(filters.private & filters.text)
async def handle_message(client, message):
    info_logger.info(f"Handle message ({message.text[:15]}...) from {message.from_user.id}")
    await init_db()
    await create_user(message.from_user.id)


if __name__ == "__main__":
    app.run()

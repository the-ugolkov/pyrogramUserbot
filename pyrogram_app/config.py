import os

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

session_file = os.getenv('session_file')
api_id = os.getenv('api_id')

app = Client(session_file, api_id=api_id)

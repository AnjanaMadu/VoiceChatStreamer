import os
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

vcusr = Client(
    SESSION,
    API_ID,
    API_HASH
)

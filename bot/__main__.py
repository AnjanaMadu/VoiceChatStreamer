from bot import vcusr
from bot import TOKEN, API_ID, API_HASH
from pyrogram import Client
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

Client(
    "VC Streamer",
    API_ID,
    API_HASH,
    bot_token=TOKEN,
    plugins={'root': 'bot.plugins'}
).start()
vcusr.run()

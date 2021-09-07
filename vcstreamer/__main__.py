'''
VoiceChatStreamer, An Telegram Bot Project
Copyright (c) 2021 Anjana Madu <https://github.com/AnjanaMadu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

from pyrogram import Client, idle
from vcstreamer import API_ID, API_HASH, TOKEN, SESSION

bot = Client(
    "bot",
    API_ID,
    API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="vcstreamer"),
)
app = Client(SESSION, API_ID, API_HASH)

bot.start()
app.start()
print("Bot Started")
idle()
print("Bot Stopped")

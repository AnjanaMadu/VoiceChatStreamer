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

import asyncio
import pyrogram
import os
from pyrogram import Client, filters
from vcstreamer import video_link_getter, yt_video_search
from vcstreamer import vctools
from vcstreamer import bot, app


@bot.on_message(filters.regex("^!stream"))
async def stream_vc(client, message):
    CHAT_ID = message.chat.id
    msg = await message.reply("__Please wait.__")
    media = message.reply_to_message
    if media:
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await message.reply("Give me a URL or Search Query. Look `!help`")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            if FINAL_URL == 404:
                return await message.reply("No videos found")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="v")
         
    try:
        group_call = vctools.group_call_factory.get_group_call()
        if group_call.is_connected: await group_call.stop()
        await group_call.join(CHAT_ID)
        await msg.edit("__Playing...__")
        await group_call.start_video(LOCAL_FILE, repeat=False)
        vctools.VIDEO_CALL[CHAT_ID] = group_call
    except Exception as e:
        await message.reply(str(e))
        return await vctools.VIDEO_CALL[CHAT_ID].stop()

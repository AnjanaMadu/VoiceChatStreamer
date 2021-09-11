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

import os
from pyrogram import Client, filters
from bot import vcusr
from bot import yt_video_search, match_url
import youtube_dl

@Client.on_message(filters.command("audio", "!"))
async def audio_dl(client, message):
    msg = await message.reply("⏳ __Please wait.__")
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __Give me a search queue__")
    if match_url(INPUT_SOURCE) is None:
        FINAL_URL = yt_video_search(INPUT_SOURCE)
    else:
        FINAL_URL = INPUT_SOURCE
    aud_opts = {
        'format':'bestaudio',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
    }
    try:
        await msg.edit("📥 __Downloading...__")
        with youtube_dl.YoutubeDL(aud_opts) as ytdl:
            ytdl_data = ytdl.extract_info(FINAL_URL, download=True)
            fname = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"`{e}`")
    await msg.edit("📤 __Uploading...__")
    await message.reply_audio(
        fname,
        caption=ytdl_data['title'],
        title=ytdl_data['title'],
        performer='VoiceChatStreamer')
    try:
        os.remove(fname)
        await msg.delete()
    except: pass
    
@Client.on_message(filters.command("video", "!"))
async def video_dl(client, message):
    msg = await message.reply("⏳ __Please wait.__")
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __Give me a search queue__")
    if match_url(INPUT_SOURCE) is None:
        FINAL_URL = yt_video_search(INPUT_SOURCE)
    else:
        FINAL_URL = INPUT_SOURCE
    vid_opts = {
        'format':'best',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
    }
    try:
        await msg.edit("📥 __Downloading...__")
        with youtube_dl.YoutubeDL(vid_opts) as ytdl:
            ytdl_data = ytdl.extract_info(FINAL_URL, download=True)
            fname = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"`{e}`")
    await msg.edit("📤 __Uploading...__")
    await message.reply_video(
        fname,
        caption=ytdl_data['title'])
    try:
        os.remove(fname)
        await msg.delete()
    except: pass

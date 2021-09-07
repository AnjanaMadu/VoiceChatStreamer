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
import pytgcalls
import pyrogram
import os
import youtube_dl
import pafy
from youtubesearchpython import VideosSearch
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")
ADMINS = os.environ.get("ADMINS")
CHAT_ID = os.environ.get("CHAT_ID")
vcusr = Client(SESSION, API_ID, API_HASH)
group_call = GroupCallFactory(vcusr, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()

async def dl_progess(current, total, msg):
    if current == total:
        percentage = current * 100 / total
        try: await msg.edit(f"Downloading. {round(percentage, 2)}%")
        except: pass

@vcusr.on_message(filters.regex("^!help$"))
async def help_vc(client, message):
    text = '''**Help Menu**
- **!urlvc** __(direct video link)__
  Ex: `!urlvc https://stream.com/music.mp4`
- **!ytvc** (audio/video) __(youtube or youtube_dl support link)__
  Ex: `!ytvc audio https://youtube.com/music`
  Ex: `!ytvc video https://youtube.com/music`
  Ex: `!ytvc audio faded` __(You can use it as a search also.)__
- **!tgvc** (audio/video) __(reply to file)__
  Ex: `!tgvc audio` __(reply to audio)__
  Ex: `!tgvc video` __(reply to video)__
- **!leavevc** __(It will leave from vc)__'''
    await message.reply(text)
    
@vcusr.on_message(filters.regex("^!urlvc"))
async def url_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    if not str(message.from_user.id) in ADMINS: return
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await message.reply("Give video URL")
    msg = await message.reply("__Please wait.__")
    try:
        if group_call.is_connected: await group_call.stop()
        await group_call.join(CHAT_ID)
        await msg.edit(f"Streaming. __{INPUT_SOURCE}__")
        await group_call.start_video(INPUT_SOURCE, repeat=False)
    except RuntimeError:
        await group_call.start_audio(INPUT_SOURCE, repeat=False)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()
    
@vcusr.on_message(filters.regex("^!leavevc$"))
async def end_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    if not str(message.from_user.id) in ADMINS: return
    await group_call.stop()
    msg = await message.reply("__Left.__")

@vcusr.on_message(filters.regex("^!ytvc (audio|video)"))
async def yt_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    if not str(message.from_user.id) in ADMINS: return
    try:
        INPUT_SOURCE = message.text.split(" ", 2)[2]
        SOURCE_FORMAT = message.text.split(" ", 2)[1]
    except IndexError: return await message.reply("Give me a format and video or keyword to search. Look `!help`")
    msg = await message.reply("__Please wait.__")
    if ("https://" in INPUT_SOURCE) or ("http://" in INPUT_SOURCE) or ("Https://" in INPUT_SOURCE):
        finalyturl = INPUT_SOURCE
    else:
        videosSearch = VideosSearch(INPUT_SOURCE, limit=1)
        videoSearchId = videosSearch.result()['result'][0]['id']
        finalyturl = f"https://www.youtube.com/watch?v={videoSearchId}"
    with youtube_dl.YoutubeDL({"videoformat": "mp4", "outtmpl": "%(id)s.%(ext)s", "keepvideo":True, "prefer_ffmpeg":False}) as yt:
        info = yt.extract_info(finalyturl, False)
    if SOURCE_FORMAT == "video":
        if "youtube.com" in finalyturl or "youtu.be" in finalyturl:
            yt_mode = "video"
            vvid = pafy.new(finalyturl)
            video_url = vvid.getbest().url
        else:
            yt_mode = "video"
            video_url = info['formats'][-1]['url']
    elif SOURCE_FORMAT == "audio":
        try:
            yt_mode = "audio"
            vvid = pafy.new(finalyturl)
            audio_url = vvid.getbestaudio().url
        except Exception as e:
            return await message.reply(str(e))
    try:
        if group_call.is_connected: await group_call.stop()
        await group_call.join(CHAT_ID)
        await msg.edit(f"Playing. __{info['title']}__")
        if yt_mode == "video":
            await group_call.start_video(video_url, repeat=False)
        elif yt_mode == "audio":
            await group_call.start_audio(audio_url, repeat=False)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@vcusr.on_message(filters.regex("^!tgvc (audio|video)$"))
async def tg_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    if not str(message.from_user.id) in ADMINS: return
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await message.reply("Give file type.")
    if not message.reply_to_message: return await message.reply("Reply to video or audio")
    msg = await message.reply("__Downloading.__")
    tgfile = await client.download_media(message=message.reply_to_message)
    try:
        if group_call.is_connected: await group_call.stop()
        await group_call.join(CHAT_ID)
        await msg.edit(f"Playing. __{os.path.basename(tgfile)}__")
        if INPUT_SOURCE == "audio":
            await group_call.start_audio(tgfile, repeat=False)
        elif INPUT_SOURCE == "video":
            await group_call.start_video(tgfile, repeat=False)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

vcusr.run()

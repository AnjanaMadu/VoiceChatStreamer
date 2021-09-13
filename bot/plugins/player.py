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

import os, asyncio, pafy
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from bot import video_link_getter, yt_video_search, match_url
from bot import vcusr, ADMINS, CHAT_ID

group_call = GroupCallFactory(vcusr).get_group_call()
music_queue = []
vc_live = False
    
async def play_or_queue(source, status, typee):
    global music_queue, vc_live, group_call
    if not group_call.is_connected:
        await group_call.join(CHAT_ID)
    if status == "add":
        if len(music_queue) == 0:
            music_queue.append({'source': source, 'type': typee})
            if typee == "audio":
                await group_call.start_audio(source, repeat=False)
                return "🚩 __Playing...__"
            elif typee == "video":
                await group_call.start_video(source, repeat=False)
                return "🚩 __Streaming...__"
        elif len(music_queue) > 0:
            music_queue.append({'source': source, 'type': typee})
            return f"🚩 __Queued at {len(music_queue)}__"
    elif status == "check":
        if len(music_queue) == 0:
            await group_call.stop()
            return "Queue empty. Leaving"
        elif len(music_queue) > 0:
            source = music_queue[0]['source']
            if music_queue[0]['type'] == "audio":
                await group_call.start_audio(source, repeat=False)
                return f"Playing {os.path.basename(source)}"
            elif music_queue[0]['type'] == "video":
                await group_call.start_video(source, repeat=False)
                return f"Streaming {os.path.basename(source)}"

@Client.on_message(filters.command("live", "!"))
async def live_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __Give me a URL__")
    if match_url(INPUT_SOURCE, key="yt") is None:
        return await msg.edit("🔎 __Give me a valid URL__")
    #ytlink = await run_cmd(f"youtube-dl -g {INPUT_SOURCE}")
    videof = pafy.new(INPUT_SOURCE)
    ytlink = videof.getbest().url
    if match_url(ytlink) is None:
        return await msg.edit(f"`{ytlink}`")
    try:
        if not group_call.is_connected:
            await group_call.join(CHAT_ID)
        else:
            await group_call.reconnect()
        await msg.edit("🚩 __Live Streaming...__")
        await group_call.start_video(ytlink, repeat=False, enable_experimental_lip_sync=True)
        vc_live = True
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@Client.on_message(filters.command("radio", "!"))
async def radio_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __All radio stations listed [here](https://github.com/AnjanaMadu/radio_stations). Please get link from [here](https://github.com/AnjanaMadu/radio_stations)__", disable_web_page_preview=True)
    if match_url(INPUT_SOURCE) is None:
        return await msg.edit("🔎 __Give me a valid URL__")
    try:
        if not group_call.is_connected:
            await group_call.join(CHAT_ID)
        else:
            await group_call.reconnect()
        await msg.edit("🚩 __Radio Playing...__")
        await group_call.start_audio(INPUT_SOURCE, repeat=False)
        vc_live = True
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()
    
@Client.on_message(filters.command("play", "!"))
async def play_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    if media:
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 __Give me a URL or Search Query. Look__ `!help`")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            if FINAL_URL == 404:
                return await msg.edit("__No videos found__ 🤷‍♂️")
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="a")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
         
    try:
        resp = await play_or_queue(LOCAL_FILE, "add", "audio")
        await msg.edit(resp)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@Client.on_message(filters.command("stream", "!"))
async def stream_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    if media:
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 __Give me a URL or Search Query. Look__ `!help`")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            if FINAL_URL == 404:
                return await msg.edit("__No videos found__ 🤷‍♂️")
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="v")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
         
    try:
        resp = await play_or_queue(LOCAL_FILE, "add", "video")
        await msg.edit(resp)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@group_call.on_playout_ended
async def playout_ended_check(gc, source, media_type):
    if len(music_queue) == 0: return
    if source == music_queue[0]['source']:
        os.remove(source)
        music_queue.pop(0)
    status = await play_or_queue(None, "check", None)
    os.system(f'echo "{status}"')

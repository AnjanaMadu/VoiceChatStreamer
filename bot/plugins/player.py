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

import os, asyncio, pafy, youtube_dl
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from bot import video_info_extract, yt_video_search, match_url
from bot import vcusr, ADMINS, CHAT_ID

group_call = GroupCallFactory(vcusr).get_group_call()
music_queue = []
vc_live = False
    
async def play_or_queue(status, data=None):
    global music_queue, group_call
    if not group_call.is_connected:
        await group_call.join(CHAT_ID)
    if status == "add":
        if len(music_queue) == 0:
            music_queue.append(data)
            if data['TYPE'] == "audio":
                await group_call.start_audio(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Playing...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
            elif data['TYPE'] == "video":
                await group_call.start_video(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Streaming...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
        elif len(music_queue) > 0:
            music_queue.append(data)
            return {"status":"queue", "msg":f"🚩 __Queued at {len(music_queue)-1}__"}
    elif status == "check":
        if len(music_queue) == 0:
            await group_call.stop()
            return {"status":"empty", "msg":"💬 __Queue empty. Leaving...__"}
        elif len(music_queue) > 0:
            data = music_queue[0]
            if data['TYPE'] == "audio":
                await group_call.start_audio(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Playing...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
            elif data['TYPE'] == "video":
                await group_call.start_video(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Streaming...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}

@Client.on_message(filters.command("endvc", "!"))
async def leave_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    await group_call.stop()
    vc_live = False
    music_queue.clear()
    await message.reply_sticker("CAADBQADCAMAAtFreFVNNKAMgNe-YwI")
    
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
            await group_call.stop()
            await asyncio.sleep(3)
            await group_call.join(CHAT_ID)
            
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
            await group_call.stop()
            await asyncio.sleep(3)
            await group_call.join(CHAT_ID)
            
        await msg.edit("🚩 __Radio Playing...__")
        await group_call.start_audio(INPUT_SOURCE, repeat=False)
        vc_live = True
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()
    
@Client.on_message(filters.command("play", "!"))
async def play_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    msg = await message.reply("⏳ __Please wait.__")
    if vc_live == True:
        return await msg.edit("💬 __Live or Radio Ongoing. Please stop it via `!endvc`.__")
    media = message.reply_to_message
    THUMB_URL, VIDEO_TITLE, VIDEO_DURATION = "https://appletld.com/wp-content/uploads/2020/10/E3593D8D-6F1C-4A16-B065-2154ED6B2355.png", "Music", "Not Found"
    if media and media.media:
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
        LOCAL_FILE, THUMB_URL, VIDEO_TITLE, VIDEO_DURATION = video_info_extract(FINAL_URL, key="audio")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
         
    try:
        post_data = {'LOCAL_FILE':LOCAL_FILE, 'THUMB_URL':THUMB_URL, 'VIDEO_TITLE':VIDEO_TITLE, 'VIDEO_DURATION':VIDEO_DURATION, 'TYPE':'audio'}
        resp = await play_or_queue("add", post_data)
        if resp['status'] == 'queue':
            await msg.edit(resp['msg'])
        elif resp['status'] == 'play':
            await msg.delete()
            await message.reply_photo(resp['thumb'], caption=resp['msg'])
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@Client.on_message(filters.command("stream", "!"))
async def stream_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    msg = await message.reply("⏳ __Please wait.__")
    if vc_live == True:
        return await msg.edit("💬 __Live or Radio Ongoing. Please stop it via `!endvc`.__")
    media = message.reply_to_message
    THUMB_URL, VIDEO_TITLE, VIDEO_DURATION = "https://appletld.com/wp-content/uploads/2020/10/E3593D8D-6F1C-4A16-B065-2154ED6B2355.png", "Music", "Not Found"
    if media and media.media:
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
        LOCAL_FILE, THUMB_URL, VIDEO_TITLE, VIDEO_DURATION = video_info_extract(FINAL_URL, key="audio")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
    try:
        post_data = {'LOCAL_FILE':LOCAL_FILE, 'THUMB_URL':THUMB_URL, 'VIDEO_TITLE':VIDEO_TITLE, 'VIDEO_DURATION':VIDEO_DURATION, 'TYPE':'video'}
        resp = await play_or_queue("add", post_data)
        if resp['status'] == 'queue':
            await msg.edit(resp['msg'])
        elif resp['status'] == 'play':
            await msg.delete()
            await message.reply_photo(resp['thumb'], caption=resp['msg'])
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@Client.on_message(filters.command("skip", "!"))
async def skip_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    if len(music_queue) == 0: return await message.reply("💬 __Nothing in queue.__")
    if group_call.is_video_running:
        await group_call.stop_media()
    elif group_call.is_audio_running:
        await group_call.stop_media()
    elif group_call.is_running:
        await group_call.stop_media()
    os.remove(music_queue[0]['LOCAL_FILE'])
    music_queue.pop(0)
    resp = await play_or_queue("check")
    if resp['status'] == 'empty':
        await message.reply(resp['msg'])
    elif resp['status'] == 'play':
        await message.reply_photo(resp['thumb'], caption=resp['msg'])
    
@group_call.on_playout_ended
async def playout_ended_check(gc, source, media_type):
    if len(music_queue) == 0: return
    if source == music_queue[0]['LOCAL_FILE']:
        os.remove(source)
        music_queue.pop(0)
    resp = await play_or_queue("check")
    if resp['status'] == 'empty':
        await Client.send_message(chat_id=CHAT_ID, text=resp['msg'])
    elif resp['status'] == 'play':
        await Client.send_photo(chat_id=CHAT_ID, photo=resp['thumb'], caption=resp['msg'])

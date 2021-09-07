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
from pytgcalls import GroupCallFactory
from pytube import YouTube
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

class config():
  API_ID = int(os.environ.get("API_ID"))
  API_HASH = os.environ.get("API_HASH")
  TOKEN = os.environ.get("TOEKN")
  SESSION = os.environ.get("SESSION")
  ADMINS = os.environ.get("ADMINS")
  CHAT_ID = int(os.environ.get("CHAT_ID"))

class vc_clients():
  bot = Client(
    "bot",
    config.API_ID,
    config.API_HASH,
    bot_token=config.TOKEN,
    plugins=dict(root="vcstreamer")
  )
  app = Client(
    config.SESSION,
    config.API_ID,
    config.API_HASH
  )

class vctools():
  STREAM = {8}
  VIDEO_CALL = {}
  group_call_factory = GroupCallFactory(vc_clients.app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
  ydl_opts = {"geo-bypass": True, "nocheckcertificate": True}
  ydl = YoutubeDL(ydl_opts)

def video_link_getter(url: str, key=None):
  yt = YouTube(url)
  if key == "v":
    x = yt.streams.filter(file_extension="mp4", res="720p")[0].download()
  elif key == "a":
    x = yt.streams.filter(mime_type="audio/webm", type="audio")[-1].download()
  return x
  
def yt_video_search(q: str):
  try:
    videosSearch = VideosSearch(q, limit=1)
    videoSearchId = videosSearch.result()['result'][0]['id']
    finalurl = f"https://www.youtube.com/watch?v={videoSearchId}"
    return finalurl
  except:
    return "Not Found"

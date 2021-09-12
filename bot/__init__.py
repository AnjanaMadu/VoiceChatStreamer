import os, sys, asyncio, re, pafy
from pyrogram import Client
from youtubesearchpython import VideosSearch
from pytube import YouTube

QUEUE = []

def str_to_int(input):
    if type(input) == list:
        output = []
        for x in input:
            output.append(int(x))
        return output
    elif type(input) == str:
        return int(input)

def load_env():
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    SESSION = os.environ.get("SESSION")
    TOKEN = os.environ.get("TOKEN")
    ADMINS = os.environ.get("ADMINS")
    ADMINS = str_to_int(ADMINS.split(" "))
    CHAT_ID = str_to_int(os.environ.get("CHAT_ID"))
    return API_ID, API_HASH, SESSION, TOKEN, ADMINS, CHAT_ID
    
if os.path.isfile("config.py"):
    from config import CONFIG, API_ID, API_HASH, SESSION, TOKEN, ADMINS, CHAT_ID
    if CONFIG:
        API_ID = int(API_ID)
        API_HASH = API_HASH
        SESSION = SESSION
        TOKEN = TOKEN
        ADMINS = ADMINS
        ADMINS = str_to_int(ADMINS.split(" "))
        CHAT_ID = str_to_int(CHAT_ID)
    else:
        API_ID, API_HASH, SESSION, TOKEN, ADMINS, CHAT_ID = load_env()

vcusr = Client(
    SESSION,
    API_ID,
    API_HASH
)

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
    
async def run_cmd(cmd):
    process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    stdout, stderr = await process.communicate()
    out = stdout.decode().strip()
    return out
    
def yt_video_search(q: str):
    try:
        videosSearch = VideosSearch(q, limit=1)
        videoSearchId = videosSearch.result()['result'][0]['id']
        finalurl = f"https://www.youtube.com/watch?v={videoSearchId}"
        return finalurl
    except:
        return 404

def match_url(url, key=None):
    if key == "yt":
        pattern = r"(youtube.com|youtu.be)"
    else:
        pattern = r"((http|https)\:\/\/)"
    result = re.search(pattern, url)
    return result

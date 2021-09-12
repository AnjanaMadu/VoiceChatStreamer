# Voice Chat Streamer
_This bot can stream audio or video files and urls in telegram voice chats :)_

![GitHub Repo stars](https://img.shields.io/github/stars/AnjanaMadu/VoiceChatStreamer?color=green&logo=github)
![GitHub forks](https://img.shields.io/github/forks/AnjanaMadu/VoiceChatStreamer?color=green&logo=github)
![TG Channel](https://img.shields.io/badge/dynamic/json?color=red&label=channel%20@harp_tech&query=subscribers&url=https%3A%2F%2Fonline-users-api.up.railway.app%2Fcheck%3Fchat%3Dharp_tech&logo=telegram)
![TG Chat](https://img.shields.io/badge/dynamic/json?color=red&label=support%20@harp_chat&query=online&url=https%3A%2F%2Fonline-users-api.up.railway.app%2Fcheck%3Fchat%3Dharp_chat&logo=telegram)

_🎯 Follow me and star this repo for more telegram bots._

## 📌 Features
- Play youtube live streams.
- Radio playing.
- Play videos from youtube in audio and video formats
- Play via youtube search
- Telegram video/audio playing
- Admin control

## 📌 Deployment
- Deploy to **Heroku**

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AnjanaMadu/VoiceChatStreamer)

- Deploy to **Railway**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2FAnjanaMadu%2FVoiceChatStreamer&envs=API_ID%2CAPI_HASH%2CSESSION%2CTOKEN%2CCHAT_ID%2CADMINS&referralCode=n3n8cH)

### 🏷 Radio Stations. [Click here](https://github.com/AnjanaMadu/radio_stations)

_If you like to add your country radio stations, Please open pull request [here](https://github.com/AnjanaMadu/radio_stations)_

### 🏷 Deployment Guide 

_Note: How to use? You need to add String session own's user to your group. Ok now you added userbot to your group. Then do `!help`. Now you can get help menu. Read it and Do what you want by reffering help menu. For help [@harp_chat](https://t.me/harp_chat)_

<details>
  <summary>How to get <code>API_ID</code> and <code>API_HASH</code></summary>
  Get <i>API_ID</i> and <i>API_HASH</i> from <a href="https://my.telegram.org/apps">here</a>. I think its easy.
</details>

<details>
  <summary>How to generate <code>SESSION</code>?</summary>
  <b>Step 1:</b> Go to <a href="https://replit.com/@AnjanaMadu/GenerateStringSession">here</a>.<br>
  <b>Step 2:</b> Click run button and wait.<br>
  <b>Step 3:</b> Not ask for option. Fill number 1.<br>
  <b>Step 4:</b> Now ask for API ID and API HASH. Fill them.<br>
  <b>Step 5:</b> Now ask for mobile fill it also.<br>
  <b>Final Step:</b> Now ask for confirmation. Fill it. TraLaa. Now check saved. String Session will be there.
</details>

- `TOKEN`: Bot Token
- `CHAT_ID`: Chat ID where bot should work
- `ADMINS`: Add ur TG ID, Seperate by spaces

### 🏷 VPS Deployment Docker

**For Linux (Ubuntu)**

- Updating package list and Install wget, git
  - `sudo apt-get update && sudo apt-get install wget git -y`
- Installing Docker
  - `wget https://get.docker.com -O get-docker.sh`
  - `sudo bash get-docker.sh`
  - `rm get-docker.sh`
- Cloning Repo and Go to dir
  - `git clone https://github.com/AnjanaMadu/VoiceChatStreamer bot`
  - `cd bot`
- _Now edit "config.py" with your values._
- Docker Build
  - `sudo docker build . -t vcstreamer`
- Start Bot
  - `sudo docker run vcstreamer`

### 🏷 VPS Deployment Without Docker

**For Linux (Ubuntu)**

- Updating package list and Install wget, git
  - `sudo apt-get update && sudo apt-get install wget git -y`
- Install pip3
  - `sudo apt install python3-pip`
- Cloning Repo and Go to dir
  - `git clone https://github.com/AnjanaMadu/VoiceChatStreamer bot`
  - `cd bot`
- _Now edit "config.py" with your values._
- Install Requirements
  - `pip3 install -U pip && pip3 install -r requirements.txt`
- Start Bot
  - `screen -S VoiceChatStreamer`
  - `python3 -m bot`
- Detach from the screen 
  - Ctrl-a Ctrl-d


## 📌 Credits
- [MarshalX](https://github.com/MarshalX/tgcalls) for Pytgcalls
- [SpEcHiDe](https://github.com/SpEcHiDe) for Multi VCs support
- [Me](https://github.com/AnjanaMadu) for this Project 🤪

## 📌 License
```
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
```

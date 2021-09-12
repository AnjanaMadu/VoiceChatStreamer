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

import os, asyncio
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from bot import vcusr, CHAT_ID, ADMINS
from bot.plugins.player import group_call, vc_live

vc_paused = False

@Client.on_message(filters.command("endvc", "!"))
async def leave_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    await group_call.stop()
    await message.reply("__Left.__")
    vc_live = False
    
@Client.on_message(filters.command("pause", "!"))
async def pause_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    if vc_paused is False:
        await group_call.set_pause(True)
        await message.reply("__VC Paused!__")
    elif vc_paused is True:
        return await message.reply("__Already Paused.__")
          
@Client.on_message(filters.command("resume", "!"))
async def resume_vc(client, message):
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    if vc_paused is True:
        await group_call.set_pause(False)
        await message.reply("__VC Resumed!__")
    elif vc_paused is False:
        return await message.reply("__VC not Paused.__")

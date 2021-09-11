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
from bot import vcusr, GROUP_CALLS

MISC_DB = {}

@Client.on_message(filters.command("endvc", "!"))
async def leave_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    group_call = GROUP_CALLS.get(CHAT_ID)
    if group_call:
        await group_call.stop()
        await message.reply("__Left.__")
    elif group_call is None:
        return await message.reply("__No VC Running.__")
        
@Client.on_message(filters.command("showdb", "!"))
async def dont_do_this_vc(client, message):
    dbz = str(GROUP_CALLS) + "\n" + str(MISC_DB)
    await message.reply(dbz)
    
@Client.on_message(filters.command("pause", "!"))
async def pause_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    group_call = GROUP_CALLS.get(CHAT_ID)
    if group_call is None:
        return await message.reply("__No VC Running.__")
    else:
        status = MISC_DB.get(CHAT_ID)
        if status is None:
            await group_call.set_pause(True)
            await message.reply("__VC Paused!__")
            MISC_DB.update({CHAT_ID: "PAUSE:True"})
        elif status == "PAUSE:False":
            await group_call.set_pause(True)
            await message.reply("__VC Paused!__")
            MISC_DB.update({CHAT_ID: "PAUSE:True"})
        elif status == "PAUSE:True":
            return await message.reply("__Already Paused.__")
          
@Client.on_message(filters.command("resume", "!"))
async def resume_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    group_call = GROUP_CALLS.get(CHAT_ID)
    if group_call is None:
        return await message.reply("__No VC Running.__")
    else:
        status = MISC_DB.get(CHAT_ID)
        if status is None:
            return await message.reply("__VC not Paused.__")
        elif status == "PAUSE:True":
            await group_call.set_pause(False)
            await message.reply("__VC Resumed!__")
            MISC_DB.pop(CHAT_ID)
        elif status == "PAUSE:False":
            return await message.reply("__VC not Paused.__")

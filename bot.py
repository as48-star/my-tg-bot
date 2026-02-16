import asyncio
import json
import re
import os
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

# --- Aapki Details ---
API_ID = 22319684
API_HASH = "17b2b31671daa77fd64c807b397d0dfc"
BOT_TOKEN = "8442918548:AAFbuDOJWk90bV-WHjMZWWGp5PfY3AuQ63o"
ADMIN_ID = 8035280106
CHANNEL_USERNAME = "backupour6" 

# Client setup bina turant start kiye
client = TelegramClient("bot_session", API_ID, API_HASH)

# User Database Setup
DB_FILE = "users.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f: json.dump([], f)

def add_user(user_id):
    try:
        with open(DB_FILE, "r") as f: users = json.load(f)
    except: users = []
    if user_id not in users:
        users.append(user_id)
        with open(DB_FILE, "w") as f: json.dump(users, f)

link_re = re.compile(r"(?:https?://)?t\.me/([a-zA-Z0-9_]+)/(\d+)")
c_link_re = re.compile(r"(?:https?://)?t\.me/c/(\d+)/(\d+)")

# Force Join Check
async def check_user_joined(user_id):
    if user_id == ADMIN_ID: return True
    try:
        await client(GetParticipantRequest(channel=CHANNEL_USERNAME, participant=user_id))
        return True
    except UserNotParticipantError: return False
    except: return False

@client.on(events.NewMessage(pattern=r"(?i)^/start"))
async def start_handler(event):
    add_user(event.sender_id)
    if not await check_user_joined(event.sender_id):
        buttons = [[Button.url("Join Channel", f"https://t.me/{CHANNEL_USERNAME}")]]
        return await event.reply("❌ **Access Denied!** Join channel first.", buttons=buttons)
    await event.reply("👋 **Bot Online!** Send me a link.")

@client.on(events.NewMessage(pattern=r"(?i)^https?://t\.me/"))
async def handler(event):
    if not await check_user_joined(event.sender_id): return
    text = event.text.strip()
    m = c_link_re.search(text) or link_re.search(text)
    if not m: return

    # Admin log
    if event.sender_id != ADMIN_ID:
        await client.send_message(ADMIN_ID, f"👤 User: `{event.sender_id}`\n🔗 Link: {text}")

    chat_id = int("-100" + m.group(1)) if "t.me/c/" in text else m.group(1)
    start_id = int(m.group(2))
    status = await event.reply("⏳ **Processing Sequence...**")

    for i in range(10):
        try:
            msg = await client.get_messages(chat_id, ids=start_id + i)
            if not msg: continue
            if msg.media: await client.send_file(event.chat_id, msg.media, caption=msg.text or "")
            elif msg.text: await client.send_message(event.chat_id, msg.text)
            await asyncio.sleep(1)
        except: continue
    await status.edit("✅ **Done!**")

# --- Render Fix: Modern Asyncio Loop ---
async def start_bot():
    # Bot ko yahan start karenge
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 Bot is successfully running on Render!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Naye Python versions ke liye sabse sahi tarika
    asyncio.run(start_bot())
    

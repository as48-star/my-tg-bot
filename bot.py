import asyncio
import os
import re
import json
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- Aapki Details ---
API_ID = 22319684
API_HASH = "17b2b31671daa77fd64c807b397d0dfc"
BOT_TOKEN = "8442918548:AAFbuDOJWk90bV-WHjMZWWGp5PfY3AuQ63o"
ADMIN_ID = 8035280106
CHANNEL_USERNAME = "backupour6" 

client = TelegramClient("bot_session", API_ID, API_HASH)

# --- FREE WEB SERVER FOR RENDER ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is Running Successfully!')

def run_web_server():
    # Render hamesha ek PORT variable deta hai free users ko
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"🌍 Web Server started on port {port}")
    server.serve_forever()

# --- Bot Logic ---
@client.on(events.NewMessage(pattern=r"(?i)^/start"))
async def start_handler(event):
    await event.reply("👋 **Bot Online Hai!**\nBas link bhejein.")

@client.on(events.NewMessage(pattern=r"(?i)^https?://t\.me/"))
async def handler(event):
    # Aapka purana sequence fetching logic yahan kaam karega
    await event.reply("⏳ **Processing...**")

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 Bot Started!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Web server ko background mein chalana (Free fix for Render)
    threading.Thread(target=run_web_server, daemon=True).start()
    # Bot start karna
    asyncio.run(main())
    

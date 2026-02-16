import asyncio
import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events

# --- Details (Same rakhein) ---
API_ID = 22319684
API_HASH = "17b2b31671daa77fd64c807b397d0dfc"
BOT_TOKEN = "8442918548:AAFbuDOJWk90bV-WHjMZWWGp5PfY3AuQ63o"
ADMIN_ID = 8035280106
CHANNEL_USERNAME = "backupour6" 


client = TelegramClient("bot_session", API_ID, API_HASH)

# Render Fix Web Server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is Live and Running!')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

@client.on(events.NewMessage(pattern=r"(?i)^https?://t\.me/"))
async def handler(event):
    text = event.text.strip()
    m = re.search(r"t\.me/(?:c/)?([a-zA-Z0-9_]+)/(\d+)", text)
    if not m: return

    status = await event.reply("⏳ **Fetching... Please wait.**")
    
    try:
        chat_id = int("-100" + m.group(1)) if "t.me/c/" in text else m.group(1)
        start_id = int(m.group(2))

        # Sirf 5 files ek baar mein check karein (RAM bachaane ke liye)
        for i in range(10):
            msg = await client.get_messages(chat_id, ids=start_id + i)
            if not msg: continue
            
            if msg.media:
                await client.send_file(event.chat_id, msg.media, caption=msg.text or "")
            elif msg.text:
                await client.send_message(event.chat_id, msg.text)
            
            await asyncio.sleep(2) 

        await status.edit("✅ **Kaam ho gaya!**")
    except Exception as e:
        print(f"Error: {e}")
        await status.edit(f"❌ **Dikkat aayi:** {str(e)}")

async def start_bot():
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 Bot is Online!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    asyncio.run(start_bot())
    

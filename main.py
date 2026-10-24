import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands
import google.generativeai as genai

# سيرفر وهمي لتجاوز فحص المنفذ في Render
def run_dummy_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive!")
        def log_message(self, format, *args):
            pass

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TOKEN = os.getenv("DISCORD_TOKEN")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

@bot.event
async def on_ready():
    print(f"Logged in successfully as {bot.user}")

@bot.command(name="ask")
async def ask(ctx, *, prompt: str):
    try:
        await ctx.send("Thinking...")
        response = gemini_model.generate_content(prompt)
        reply_text = response.text
        
        await ctx.send(f"**Reply:**\n{reply_text}")
            
    except Exception as e:
        await ctx.send(f"Error: {e}")

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN is missing from Environment Variables.")

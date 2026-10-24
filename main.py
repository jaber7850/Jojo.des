import os
import discord
from discord.ext import commands
import google.generativeai as genai
from gtts import gTTS

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# جلب المفاتيح من المتغيرات البيئية في Render
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TOKEN = os.getenv("DISCORD_TOKEN")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-pro")

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
        
        tts = gTTS(text=reply_text, lang='ar')
        tts.save("response.mp3")
        
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if not ctx.voice_client:
                await channel.connect()
            
            voice_client = ctx.voice_client
            if voice_client.is_playing():
                voice_client.stop()
                
            voice_client.play(discord.FFmpegPCMAudio("response.mp3"))
        else:
            await ctx.send("Replied in text, but you are not connected to a voice channel.")
            
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")
    else:
        await ctx.send("Bot is not in a voice channel.")

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN is missing from Environment Variables.")

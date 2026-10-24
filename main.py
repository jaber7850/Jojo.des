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

# ضع مفتاح جمناي هنا بين علامتي التنصيص
GEMINI_API_KEY = "AQ.Ab8RN6La-myGTydWnLBH7EbQloOD7u9uOAN_bOuRbWuMfri-2g"
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

TOKEN = "MTU2MzMyNDQwMTkzODcyNjk1Mw.G8AIIY.M8AvbxqlRtitG8UBA7v8gqbWgf0Tj8sUuSX-bU"
bot.run(TOKEN)

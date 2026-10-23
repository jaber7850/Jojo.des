import os
import discord
from discord.ext import commands
import google.generativeai as genai
from gtts import gTTS

# إعدادات الصلاحيات الأساسية للبوت
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# إعداد مفتاح الذكاء الاصطناعي (Google Gemini)
# سنستبدل "ضع_مفتاح_جمناي_هنا" بمفتاحك الخاص لاحقاً
GEMINI_API_KEY = "ضع_مفتاح_جمناي_هنا"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")

@bot.command(name="انضم")
async def join_voice(ctx):
    """أمر ليقوم البوت بالدخول إلى الروم الصوتي الذي تتواجد فيه"""
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"تم الانضمام إلى الروم الصوتي: {channel.name}")
    else:
        await ctx.send("يجب أن تكون في روم صوتي أولاً يا غالي!")

@bot.command(name="تحدث")
async def talk_with_ai(ctx, *, message: str):
    """أمر لتسأل البوت سؤالاً فيرد عليك بصوت عربي داخل الروم الصوتي"""
    try:
        # 1. توليد الرد من نموذج جمناي باللغة العربية
        response = gemini_model.generate_content(f"أجب باختصار شديد وباللغة العربية على التالي: {message}")
        reply_text = response.text
        
        await ctx.send(f"**الرد:** {reply_text}")

        # 2. تحويل النص العربي إلى صوت باستخدام gTTS
        tts = gTTS(text=reply_text, lang='ar')
        audio_file = "response.mp3"
        tts.save(audio_file)

        # 3. التأكد من أن البوت متصل بالروم الصوتي لتشغيل الصوت
        if ctx.voice_client and ctx.voice_client.is_connected():
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            
            source = discord.FFmpegPCMAudio(audio_file)
            ctx.voice_client.play(source, after=lambda e: print(f'انتهى التشغيل: {e}'))
        else:
            await ctx.send("البوت ليس متصلاً بروم صوتي! استخدم أمر !انضم أولاً.")

    except Exception as e:
        await ctx.send(fحدث خطأ: {e}")

@bot.command(name="اطلع")
async def leave_voice(ctx):
    """أمر ليخرج البوت من الروم الصوتي"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("تم قطع الاتصال والخروج من الروم الصوتي.")
    else:
        await ctx.send("البوت ليس في روم صوتي أصلاً.")

# تشغيل البوت باستخدام التوكن الخاص بك
# سنستبدل "ضع_التوكن_هنا" برمز التوكن الذي نسخته من موقع ديسورد
TOKEN = "ضع_التوكن_هنا"
bot.run(TOKEN)

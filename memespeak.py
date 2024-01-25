import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os


on_ready_afk = True  # Set false to not have bot autojoin AFK Channel.

load_dotenv()

bot_key = os.getenv("BOT_KEY")
restricted_channel_id = None
the_sound = ''

intents = discord.Intents.default()

intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='!')

async def play_sound(vc, the_sound):
    vc.play(discord.FFmpegPCMAudio(source=the_sound, ))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
        
@bot.event
async def on_ready():
    if on_ready_afk == True:
        print(f"Logged in as {bot.user}")
    else:
        return

# Bot listens for member voice channel update   
@bot.listen()
async def on_voice_state_update(member, before, after):
    
    if member.bot or before.channel == after.channel:
        return
    
    if after.channel and len(after.channel.members) > 1:
        try:
            vc = await after.channel.connect()
            the_sound = 'resources/audio/join.mp3'
            await play_sound(vc, the_sound)
            
        except discord.ClientException as e:
            pass
    
    if before.channel and not after.channel:
        try:
            vc = await before.channel.connect()
            the_sound = './resources/audio/leave.mp3'
            await play_sound(vc, the_sound)
            
        except discord.ClientException as e:
            pass
                    
    if before.channel and after.channel and before.channel != after.channel:
        try:
            vc = await after.channel.connect(vc, the_sound)
            the_sound = './resources/audio/moved.mp3'
            await play_sound()
            
        except discord.ClientException as e:
            pass
    

            
bot.run(bot_key)
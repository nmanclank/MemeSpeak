import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

bot_key = os.getenv("BOT_KEY")
restricted_channel_id = os.getenv("RESTRICTED_CHANNEL_ID")

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def play_sound(vc, sound_path):
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=sound_path))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot or before.channel == after.channel:
        return

    restricted_channel_id = 1095538701829939320

    if after.channel and after.channel.id == restricted_channel_id:
        return

    afk_channel = member.guild.afk_channel

    if after.channel and len(after.channel.members) > 1:
        vc = await after.channel.connect()
        await play_sound(vc, "./resources/audio/join.mp3")
        if afk_channel:
            await vc.move_to(afk_channel)

    if before.channel and not after.channel:
        vc = await before.channel.connect()
        await play_sound(vc, "./resources/audio/leave.mp3")
        if afk_channel:
            await vc.move_to(afk_channel)

    if before.channel and after.channel and before.channel != after.channel:
        vc = await after.channel.connect()
        await play_sound(vc, "./resources/audio/moved.mp3")
        if afk_channel:
            await vc.move_to(afk_channel)
            
bot.run(bot_key)
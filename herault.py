# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pprint
import time

pp = pprint.PrettyPrinter(indent=0)

load_dotenv(dotenv_path=".env")

###############################
# GLOBAL VARIABLE
###############################
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='°')

@bot.event
async def on_ready():
    print("bot online")
@bot.command()
async def join(ctx):
    chan = ctx.message.author.voice.channel
    print(chan.name)
    if chan is None:
       await ctx.send("vous devez etre en vocal ;)")
    else:
        await chan.connect()


async def play(ctx, vocal):
    print("play")
    vc = await vocal.connect()
    player = discord.FFmpegPCMAudio('song.mp3')
    print(vc, player)
    await vc.play(player)
    while vc.is_playing():
        time.sleep(1)
    await vc.disconnect()


@bot.command(name='replique')
async def replique(ctx):
    await ctx.send(content="hasta la vista baby", tts=True)


@bot.command(name='speak')
async def speak(ctx,words):
    os.system(f"rm speak.mp3 || true")
    os.system(f"echo \"{words}\" | espeak -v fr -s 130 --stdout | ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 speak.mp3")
    time.sleep(5)
    await play(ctx, ctx.message.author.voice.channel)
    #for voice in ctx.guild.voice_channels:
    #    if len(voice.members) >= 0:
    #        await play(ctx, voice)


bot.run(TOKEN)

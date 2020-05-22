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
TOKEN = os.getenv('DISCORD_TOKEN_INIB')

bot = commands.Bot(command_prefix='^')

ignored = None
def get_user_from_mention(mention):
    id = ""
    for elt in mention:
        if elt in [str(e) for e in range(0,10)]:
            id += elt
    return id
@bot.command(name="inib")
async def inib(ctx, name):
    global ignored

    #print(get_user_from_mention(name), get_user_from_mention(ctx.author.mention),ctx.author.id)
    if ctx.author.id == ignored:
        await ctx.send("Action impossible désolé :/")
        return
    if name == "None":
        ignored = None
        return
    ignored = int(get_user_from_mention(name))
    guild = ctx.guild
    me = discord.utils.get(guild.members, id=bot.user.id)
    inib_member = discord.utils.get(guild.members, id=ignored)
    print(me, inib_member)
    if inib_member is not None and me is not None:
        print(me)
        await me.edit(nick=inib_member.display_name)
        avatar = inib_member.avatar_url
        await avatar.save(".\\avatar")
        a = open(".\\avatar", "rb")
        await bot.user.edit(avatar=a.read())

@bot.command(name="inib-id")
async def inib(ctx, id):
    global ignored

    #print(get_user_from_mention(name), get_user_from_mention(ctx.author.mention),ctx.author.id)
    if ctx.author.id == ignored:
        await ctx.send("Action impossible désolé :/")
        return
    if id == "None":
        ignored = None
        return
    ignored = id
    guild = ctx.guild
    me = discord.utils.get(guild.members, id=bot.user.id)
    inib_member = discord.utils.get(guild.members, id=ignored)
    print(me, inib_member)
    if inib_member is not None and me is not None:
        print(me)
        await me.edit(nick=inib_member.display_name)
        avatar = inib_member.avatar_url
        await avatar.save(".\\avatar")
        a = open(".\\avatar", "rb")
        await bot.user.edit(avatar=a.read())



@bot.command()
async def join(ctx):
    chan = ctx.message.author.voice.channel
    print(chan.name)
    if chan is None:
       await ctx.send("vous devez etre en vocal ;)")
    else:
        await chan.connect()
@bot.command()
async def quit(ctx):
    if ctx.author.id == ignored:
        await ctx.send("Action impossible désolé :/")
        return
    me = discord.utils.get(ctx.guild.members, id=bot.user.id)
    await me.move_to(None)

@bot.event
async def on_voice_state_update(member, before, after):
    global ignored

    if member.id == ignored:
        print("ignored move")
        me = discord.utils.get(member.guild.members, id=bot.user.id)
        if me.voice is not None:
            if after.channel == me.voice.channel and me.voice.channel is not None:
                print("In same chan !!!")
                await member.move_to(None)


bot.run(TOKEN)

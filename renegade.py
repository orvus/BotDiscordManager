# bot.py
import os
import asyncio
import random
import time
import discord
from discord.ext import commands
import copy
from dotenv import load_dotenv
import pickle
import urllib.request
import wget


load_dotenv(dotenv_path=".env")

bot = commands.Bot(command_prefix='~')
###############################
# GLOBAL VARIABLE
###############################
TOKEN = os.getenv('DISCORD_TOKEN')

################################
################################
################################

################
# BOT COMMAND  #
################
## GET STATE OF BOT ##
count = 0

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    if after is not None and after.channel is not None and after.channel.id == 693214496805748796 and "-18 ans" in [role.name for role in member.roles]:
        await member.move_to(None)

@bot.command(name='renegadeVOTE')
async def send_beer2(ctx, user):
    print(user,user[3:-1])
    print(discord.utils.get(ctx.guild.members, id=int(user[3:-1])))



@bot.command(name='renegade')
async def send_beer(ctx, user):
    await ctx.message.delete(delay=0)
    guild = ctx.guild
    user = discord.utils.get(guild.members, display_name=user)
    private_chan = await user.create_dm()
    await private_chan.send("voici ta bière pour la renegade",file=discord.File(f".\\plop.png"))
    await ctx.send(f"{user.mention} a reçu une bière pour la renegade ;) ", file=discord.File(f".\\plop.png"))
    print(f"beer send to {user.name}")
@bot.command(name='defi')
async def send_beer(ctx, user):
    await ctx.message.delete(delay=0)
    guild = ctx.guild
    user = discord.utils.get(guild.members, display_name=user)
    private_chan = await user.create_dm()
    await private_chan.send("voici ta bière pour le défi siteswap",file=discord.File(f".\\plop.png"))
    await ctx.send(f"{user.mention} a reçu une bière pour le défi siteswap ;) ", file=discord.File(f".\\plop.png"))
    print(f"beer send to {user.name}")


@bot.command(name="random")
async def choose_random(ctx, badge="Conventionniste"):
    if "Doom Guy" in [role.name for role in ctx.author.roles]:
        list_member = [member for member in ctx.guild.members if badge in [role.name for role in member.roles]]
        print(len(list_member), f" {badge}")
        choosen_one = random.choice(list_member)
        await ctx.send(f"{choosen_one.mention}, Bravo tu as été choisi")
    else:
        await ctx.send(f"désolé, tu n'as pas les droits :/")


@bot.command(name="count")
async def count(ctx):
    await ctx.send(f"{len(ctx.guild.members)}, Sur le serveur")

@bot.command(name="countMember")
async def count(ctx,badge):
    list_member = [member for member in ctx.guild.members if badge in [role.name for role in member.roles]]
    await ctx.send(f"{len(list_member)}, avec le badge {badge}")

@bot.command(name="countForTICKET")
async def countfor(ctx):
    print("plop")
    l = ["TICKET LOTERIE "+str(i) for i in range(1,8)]
    for r in l:
        print(f"{r}")
        list_member = [member for member in ctx.guild.members if r in [role.name for role in member.roles]]
        print(f"{len(list_member)}")
        await ctx.send(f"{len(list_member)}, Sur le badge {r}")



@bot.command(name="dl")
async def test_dl(ctx, canal_id, id_msg):
    canal = discord.utils.get(ctx.guild.channels, id=int(canal_id))
    msg = await canal.fetch_message(int(id_msg))

    a = "".join([plop.url for plop in msg.attachments])
    await ctx.send(a)







bot.run(TOKEN)

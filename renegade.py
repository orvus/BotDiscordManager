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

def emoji_get_id(emoji):
    print(type(emoji), emoji)
    if type(emoji) is str:
        return emoji
    if type(emoji) is discord.PartialEmoji:
        print("partial")
        if emoji.is_custom_emoji():
            return emoji.id
        if emoji.is_unicode_emoji():
            return emoji.name
    else:
        return emoji.id


emoji = {"oui": None, "non" : None}
msg = None
audio = None


def get_values(obj,tab,attr):
    return list(map(lambda tmp: getattr(tmp, attr), getattr(obj, tab)))

@bot.command()
async def configure_renegade(ctx,chan_audio):
    def check(reaction, user):
        return user == ctx.author and reaction.message.id == ctx.message.id  # and str(reaction.emoji) == '👍'

    await ctx.send("waiting reaction for the message above")
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        reaction2, user2 = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('👎')
        return
    emoji["oui"] = emoji_get_id(reaction.emoji)
    emoji["non"] = emoji_get_id(reaction2.emoji)
    audio = chan_audio


@bot.command(name='renegade2')
async def send_beer2(ctx, user):
    global msg
    await ctx.message.delete(delay=0)
    user = discord.utils.get(ctx.guild.members, display_name=user)
    msg = await ctx.send(f"{user.mention} a-t-il mérité ça bière ? vote avec les émoji ;)")

    msg.add_reaction(emoji["oui"])
    msg.add_reaction(emoji["non"])

@bot.event
async def on_raw_reaction_add(reactionPayload):
    global msg
    msg_id = reactionPayload.message_id
    emoji_real = reactionPayload.emoji
    member = reactionPayload.member
    guild = member.guild
    emoji = emoji_get_id(emoji_real)
    if msg is None:
        return
    if msg_id != msg.id:
        return
    if member.id not in get_values(audio,"members","name"):
        return
    for react in msg.reactions:
        if emoji_get_id(react.emoji) == emoji["oui"]:
            if react.count >= len(audio.members)/3:
                msg.channel.send("ok")
                msg = None
                return
        if emoji_get_id(react.emoji) == emoji["non"]:
            if react.count >= len(audio.members)/3:
                msg.channel.send("nok")
                msg = None
                return


@bot.command(name='renegade')
async def send_beer(ctx, user):
    await ctx.message.delete(delay=0)
    guild = ctx.guild
    user = discord.utils.get(guild.members, display_name=user)
    private_chan = await user.create_dm()
    await private_chan.send("voila ta bière pour la renegade",file=discord.File(f".\\beer.png"))
    await ctx.send(f"{user.mention} a reçu une bière pour la renegade ;) ", file=discord.File(f".\\beer.png"))
    print(f"beer send to {user.name}")


@bot.command(name='bière',aliases=["biere"])
async def send_beer(ctx, user):
    await ctx.message.delete(delay=0)
    guild = ctx.guild
    user = discord.utils.get(guild.members, display_name=user)
    private_chan = await user.create_dm()
    await private_chan.send("voilà ta bière, tu l'as méritée",file=discord.File(f".\\beer.png"))
    await ctx.send(f"{user.mention} voilà ta bière, tu l'as méritée", file=discord.File(f".\\beer.png"))
    print(f"beer send to {user.name}")

familly = []

@bot.command(name="add-familly")
async def addFamilly(ctx, a_familly):
    if a_familly not in familly:
        familly.append(a_familly)


@bot.command(name="del-familly")
async def delFamilly(ctx, a_familly):
    if a_familly in familly:
        familly.remove(a_familly)


@bot.command(name="launchFamilly")
async def launchGame(ctx, nb_familly, nb_card_per_familly):
    if len(familly) < nb_familly:
        return
    card= ["roi","dame","valet","equiyer",""]

@bot.event
async def on_member_update(before, after):
    #print(after.display_name)
    if after.nick is not None:
        if after.nick.startswith("🦆fan de Aka"):
            a = discord.utils.get(before.guild.roles, name="Fan de Aka")
            print(a.name)
            if "Fan de Aka" not in [role.name for role in before.roles]:
                await after.add_roles(discord.utils.get(before.guild.roles, name="Fan de Aka"))
                private_chan = await after.create_dm()
                await private_chan.send("Tu as été contaminé par le virus \"Fan de Aka\", pour contaminer les autres, renmome les avec 🦆fan de Aka # et met le numéro que tu veux après le '#' ;) ")
                print(f"after : {after.nick}")
    return

bot.run(TOKEN)

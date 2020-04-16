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

load_dotenv(dotenv_path=".env")

bot = commands.Bot(command_prefix='µ')
###############################
# GLOBAL VARIABLE
###############################
TOKEN = os.getenv('DISCORD_TOKEN')

to_react = dict()
GUILD = []


def save_to_react():
    with open("react2", "wb+") as f:
        f.write(pickle.dumps(to_react))

def load_to_react():
    return
    global to_react
    with open("react2", "rb") as f:
        to_react = pickle.load(f)

    for k,v in to_react.items():
        print(k,v)

################################
################################
################################


def getChanFromId(guild, _id):
    return discord.utils.get(guild.channels, id=int(_id))


def getUserFromId(guild, _id):
    return discord.utils.get(guild.members, id=int(_id))
#######################################

################
# BOT COMMAND  #
################
## GET STATE OF BOT ##
## ADD reaction roles ##
@bot.command(name='role2')
async def add_role(ctx, id_msg : int , emoji, role, type_):

    if id_msg not in to_react.keys():
        to_react[id_msg] = list()
    for react in to_react[id_msg]:
        if react["reaction"] == emoji.id and react["role_name"] == role:
            await ctx.send("role already present for this message")
            break
    else:
        to_react[id_msg].append({"reaction": emoji.id, "role_name": role, "type":int(type_)})
        await ctx.send("reaction role added")
        save_to_react()



# to_rect[msg_id] = [{"emoji" : emoji_id, "roles": [liste roles]}]
# to_rect[msg_id] = {emoji_id : [liste roles], id2 : roles}


@bot.command(name='role')
async def add_role(ctx, id_msg : int , emoji, role, type_):

    if id_msg not in to_react.keys():
        to_react[id_msg] = dict()
    if emoji.id not in to_react[id_msg].keys():
        to_react[id_msg][emoji.id] = [role]
    elif role not in to_react[id_msg][emoji.id]:
        to_react[id_msg][emoji.id].append(role)
    else:
        await ctx.send("role already in message")
    await ctx.send("reaction role added")
    save_to_react()

@bot.command(name='del-emoji')
async def del_role(ctx, id_msg, emoji):
    to_del = -1
    if id_msg not in to_react.keys():
        await ctx.send("no role register for this message")
        return
    if emoji.id not in to_react[id_msg].keys():
        await ctx.send("emoji not in message")
        return
    del to_react[id_msg][emoji.id]

@bot.command(name='del-role')
async def del_role(ctx, id_msg, role):
    to_del = -1
    if id_msg not in to_react.keys():
        await ctx.send("no role register for this message")
        return
    for emoji_id,roles in to_react[id_msg].items():
        if role in roles:
            to_react[id_msg][emoji_id].remove(role)
    await ctx.send("emoji not in message")

@bot.command(name='del-emoji-role')
async def del_emoji_role(ctx, id_msg, emoji, role):
    if id_msg not in to_react.keys():
        await ctx.send("no role register for this message")
        return
    if emoji.id not in to_react[id_msg].keys():
        await ctx.send("emoji not in message")
        return
    if role in to_react[id_msg][emoji.id]:
        to_react[id_msg][emoji.id].remove(role)
    await ctx.send("emoji not in message")


@bot.command(name='open-conv')
async def start_conv(ctx, state1, state2):
    #swap "Bénévole montage" en "Conventionniste"
    guild = ctx.guild
    role1 = discord.utils.get(guild.roles, name=state1)
    role2 = discord.utils.get(guild.roles, name=state2)
    for member in guild.members:
        print(f"{member.display_name}")
        await member.remove_roles(role1)
        await member.add_roles(role2)

    await ctx.send("Convention open")


@bot.command(name='get-archi')
async def start_bot(ctx):
    guild = ctx.guild
    s = ""
    for cat in guild.categories:
        print(f"{cat.name}\n")
        for k,v in cat.overwrites.items():
            print(f"role changé {k} \n")
            for permission in v:
                print(permission)

    #await ctx.send(discord.utils.escape_mentions(s)[:1999])

def get_element(emo_id):


@bot.event
async def on_raw_reaction_add(reactionPayload):
    global GUILD
    msg_id = reactionPayload.message_id
    emoji = reactionPayload.emoji
    member = reactionPayload.member
    guild = member.guild
    print(emoji)
    if msg_id in to_react.keys():
        rr = None
        for r in to_react[msg_id]:
            if emoji.id == r["reaction"]:
                rr = r

        if rr is not None:
            if to_react[msg_id]["type"] in [1, 2]:
                print(f"give the role {to_react[msg_id]['role']} to {member.display_name}")
                role = discord.utils.get(guild.roles, name=to_react[msg_id]["role"])
                print(f"ROLE : {to_react[msg_id]['role']}")
                if to_react[msg_id]["role"] == "Besoin d'aide":
                    print("4")
                    # send message to helper
                    print("ajout du role besoin d'aide")
                    member_roles = [role.name for role in member.roles]
                    if "Besoin d'aide" not in member_roles:
                        print("le member n'a pas deja besoin d'aide ")
                        english = "Non"
                        if ("English-speaking" in member_roles):
                            english = "Yes"
                            print("il est anglais")

                        chan_txt = discord.utils.get(guild.channels, id=694694363942354985)
                        role_to_ping = discord.utils.get(guild.roles, name="Bénévole")  # TODO orga
                        role_to_ping2 = discord.utils.get(guild.roles, name="Orga")  # TODO orga

                        await chan_txt.send(
                            f"{role_to_ping.mention} et {role_to_ping2.mention}, {member.display_name} a besoin de vous (English people : \"{english}\") ",
                            delete_after=1800)
                await member.add_roles(role)

            if to_react[msg_id]["type"] in [4]:
                print(f"remove the role {to_react[msg_id]['role']} to {member.display_name}")
                role = discord.utils.get(guild.roles, name=to_react[msg_id]["role"])
                await member.remove_roles(role)

            if guild.id not in [guild.id for guild in GUILD]:
                print("append guild not found")
                GUILD.append(guild)
            else:
                print("guild  found add to it")
                for i in range(len(GUILD)):
                    if GUILD[i].id == guild.id:
                        print(f"guild id {GUILD[i].id} at {i}")
                        GUILD[i] = guild




@bot.event
async def on_raw_reaction_remove(reactionPayload):
    global GUILD
    msg_id = reactionPayload.message_id
    emoji = reactionPayload.emoji
    guild_id = reactionPayload.guild_id
    user_id = reactionPayload.user_id
    print(f"{discord.utils.get(bot.guilds,id=guild_id).name} <------- TEST")



    if msg_id in to_react.keys():
        if to_react[msg_id]["reaction"] == emoji.name and to_react[msg_id]["type"] in [1, 3]:
            for g in GUILD:
                if g.id == guild_id:
                    guild = g
                    print(f" guild found {g.id}")
            member = discord.utils.get(guild.members, id=user_id)
            if to_react[msg_id]["role"] == "Conventionniste":
                for key,value in to_react.items():
                    if value["role"] not in ["Besoin d'aide", "-18 ans", "English-speaking"]:
                        await deleteRole(guild, member, value["role"])
            else:
                await deleteRole(guild, member, to_react[msg_id]["role"])



async def deleteRole(guild,member,role_name):
    print(f"delete the role {role_name} to {member.display_name}")
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        print(f"{role_name} n'hesite pas sur ce serveur")
    else:
        await member.remove_roles(role)

@bot.event
async def on_member_join(member):
    global GUILD
    guild = member.guild
    if guild.id not in [guild.id for guild in GUILD]:
        print(f" guild not found {guild.id} ")
        GUILD.append(guild)
    else:
        for i in range(len(GUILD)):
            if GUILD[i].id == guild.id:
                print(f"guild id {GUILD[i].id} at {i}")
                GUILD[i] = guild

print("++++++++++++++++++++++++++")
load_to_react()
print("-------------------------")
print(TOKEN)
bot.run(TOKEN)

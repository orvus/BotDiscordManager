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
            break
    else:
        to_react[id_msg].append({"reaction": emoji.id, "role_name": role, "type":int(type_)})
    await ctx.send("reaction role added")
    save_to_react()

@bot.command(name='role-del')
async def del_role(ctx, id_msg, emoji, role):
    to_del = -1
    if id_msg not in to_react.keys():
        await ctx.send("no role register for this message")
        return
    for i in range(to_react[id_msg]):
        if to_react[id_msg][i]["reation"] == emoji.id and to_react[id_msg][i]["role_name"] == role:
            to_del = i
            break

    del to_react[id_msg][to_del]
    await ctx.send("reaction role delete")
    save_to_react()
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

@bot.command(name='startbot')
async def start_bot(ctx):
    global GUILD
    GUILD.append(ctx.guild)
    await ctx.send("guild update")


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


@bot.event
async def on_raw_reaction_add(reactionPayload):
    global GUILD
    msg_id = reactionPayload.message_id
    emoji = reactionPayload.emoji
    member = reactionPayload.member
    guild = member.guild
    print(emoji)
    if msg_id in to_react.keys():

        try:
            test = to_react[msg_id]["reaction"].split(":")[1]
            print("1", emoji, emoji.name, test, emoji.name == test)
            role = discord.utils.get(guild.roles, name=to_react[msg_id]["role"])
            await member.add_roles(role)
            return
        except:
            print("ok")

        if to_react[msg_id]["reaction"] == emoji.name:
            print("2")
            if to_react[msg_id]["type"] in [1, 2]:
                print("3")
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

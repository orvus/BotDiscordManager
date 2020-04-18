# bot.py
import os
import time
import asyncio
import random
import time
import discord
from discord.ext import commands
import copy
from dotenv import load_dotenv
import pickle
from pprint import pprint

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
    global to_react
    try:
        with open("react2", "rb") as f:
            to_react = pickle.load(f)
    except:
        to_react = dict()
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

@bot.command(name="dump")
async def dump_to_react(ctx):
    pprint(to_react)


@bot.command(name='role')
async def add_role(ctx, chan_id : int, id_msg : int , role, type_: int):
    def check(reaction, user):
        return user == ctx.author  # and str(reaction.emoji) == '👍'

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('👎')
    else:
        await ctx.send('👍')
        emoji = emoji_get_id(reaction.emoji)
        if id_msg not in to_react.keys():
            to_react[id_msg] = {"chan_id": chan_id}
        if emoji not in to_react[id_msg].keys():
            to_react[id_msg][emoji] = [(role, int(type_))]
        elif role not in to_react[id_msg][emoji]:
            to_react[id_msg][emoji].append((role, int(type_)))
        else:
            await ctx.send("role already in message")
        await ctx.send("reaction role added")

        save_to_react()
        pprint(to_react)
        # react on the message
        cat = discord.utils.get(ctx.guild.channels, id=chan_id)

        await (await cat.fetch_message(id_msg)).add_reaction(reaction.emoji)

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
    pprint(to_react)

@bot.command(name='del-role')
async def del_role(ctx, id_msg, role):
    to_del = -1
    if id_msg not in to_react.keys():
        await ctx.send("no role register for this message")
        return
    for emoji_id,(roles, type_) in to_react[id_msg].items():
        if role in roles:
            to_react[id_msg][emoji_id].remove(role)
    await ctx.send("emoji not in message")
    pprint(to_react)

@bot.command(name='del-emoji-role')
async def del_emoji_role(ctx, id_msg : int, role):
    def check(reaction, user):
        return user == ctx.author  # and str(reaction.emoji) == '👍'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('👎')
    else:
        await ctx.send('👍')
        emoji = emoji_get_id(reaction.emoji)
        if id_msg not in to_react.keys():
            await ctx.send("no role register for this message")
            return
        if emoji not in to_react[id_msg].keys():
            await ctx.send("emoji not in message")
            return
        new_list = [(rrole,type_) for rrole, type_ in to_react[id_msg][emoji] if role != rrole]
        print(new_list)
        if new_list == []:
            print("empty")
            del to_react[id_msg][emoji]
            chan = discord.utils.get(ctx.guild.channels, id=to_react[id_msg]["chan_id"])
            await (await chan.fetch_message(id_msg)).add_reaction(reaction.emoji)
            if to_react[id_msg] == {}:
                del to_react[id_msg]
        else:
            print("not empty")
            to_react[id_msg][emoji] = new_list
        await ctx.send("role delted")
        pprint(to_react)
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
    pass

@bot.event
async def on_raw_reaction_add(reactionPayload):
    msg_id = reactionPayload.message_id
    emoji = reactionPayload.emoji
    member = reactionPayload.member
    guild = member.guild
    print("---- reaction add ----")
    pprint(guild)
    g2 = await bot.fetch_guild(guild.id)
    pprint(g2)
    for g in bot.guilds:
        if g.id == guild.id:
            pprint(g)
    print(emoji)
    emoji = emoji_get_id(emoji)
    print(emoji)
    #pprint(to_react)
    if msg_id in to_react.keys():
        print("1")
        a = [elt for elt in to_react[msg_id].keys()]
        a.append(emoji)
        print(a)
        if emoji in to_react[msg_id].keys():
            print("2")
            for role_name, type_ in to_react[msg_id][emoji]:
                print("3",role_name,type_)
                if type_ in [1, 2]:
                    print(f"give the role {role_name} to {member.display_name}")
                    role = discord.utils.get(guild.roles, name=role_name)
                    print(f"ROLE : {role_name}")

                    if role_name == "Besoin d'aide":  # NOT FLEXIBLE
                        # send message to helper
                        print("ajout du role besoin d'aide")
                        member_roles = [role.name for role in member.roles]
                        if "Besoin d'aide" not in member_roles:
                            print("le member n'a pas deja besoin d'aide ")
                            english = "Non"
                            if ("English-speaking" in member_roles):
                                english = "Yes"
                                print("il est anglais")

                            chan_txt = discord.utils.get(guild.channels, id=694694363942354985)  # to def later
                            role_to_ping = discord.utils.get(guild.roles, name="Bénévole")
                            role_to_ping2 = discord.utils.get(guild.roles, name="Orga")

                            #await chan_txt.send(
                                #f"{role_to_ping.mention} et {role_to_ping2.mention}, {member.display_name} a besoin de vous (English people : \"{english}\") ",
                                #delete_after=1800)
                    await member.add_roles(role)
                else:
                    print("nop")
                if type_ in [4]:
                    print(f"remove the role {role_name} to {member.display_name}")
                    role = discord.utils.get(guild.roles, name=role_name)
                    await member.remove_roles(role)

def get_values(obj,tab,attr):
    return list(map(lambda tmp: getattr(tmp, attr), getattr(obj, tab)))


@bot.event
async def on_raw_reaction_remove(reactionPayload):
    msg_id = reactionPayload.message_id
    emoji = emoji_get_id(reactionPayload.emoji)
    guild_id = reactionPayload.guild_id
    user_id = reactionPayload.user_id

    guild = discord.utils.get(bot.guilds,id=guild_id)  #await bot.fetch_guild(guild_id)
    member = discord.utils.get(guild.members,id=user_id)
    pprint(guild)
    print(f"{guild.name} {member} <------- TEST")
    if msg_id in to_react.keys():
        if emoji in to_react[msg_id].keys():
            print("2")
            for role_name, type_ in to_react[msg_id][emoji]:
                print("3",role_name,type_)
                if type_ in [1, 3]:
                    await deleteRole(guild, member, role_name)



async def deleteRole(guild,member,role_name):
    pass
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

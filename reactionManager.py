# bot.py
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import pprint
from utils import *

newintents = discord.Intents.default()
newintents.members = True


pp = pprint.PrettyPrinter(indent=0)

load_dotenv(dotenv_path=".env")

bot = commands.Bot(command_prefix='?', guild_subscriptions=True, fetch_offline_members=True, intents=newintents)
###############################
# GLOBAL VARIABLE
###############################
TOKEN = os.getenv('DISCORD_TOKEN')

to_react = dict()
GUILD = []

################################
################################
################################
def get_values(obj,tab,attr):
    return list(map(lambda tmp: getattr(tmp, attr), getattr(obj, tab)))

def getChanFromId(guild, _id):
    return discord.utils.get(guild.channels, id=int(_id))


def getUserFromId(guild, _id):
    return discord.utils.get(guild.members, id=int(_id))
#######################################


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


################
# BOT COMMAND  #
################

## DEBUG ##
@bot.command(name="dump")
async def dump_to_react(ctx):
    pp.pprint(to_react)
    await ctx.send("`" + pp.pformat(to_react) + "`")
## GET STATE OF BOT ##


#reset
@bot.command(name="reset")
async def reset_all(ctx):
    global to_react
    to_react = dict()
    save(to_react,"to_react")
    await ctx.send("all roles on reactions have been remove")

## ADD reaction roles ##
@bot.command(name='role')
async def add_role(ctx, chan_id : int, id_msg : int , role, type_: int):
    print("[add role]")
    if role not in get_values(ctx.guild, "roles", "name"):
        await ctx.send("this role doesn't exist in this server")
        return
    def check(reaction, user):
        return user == ctx.author and reaction.message.id == ctx.message.id  # and str(reaction.emoji) == '👍'
    await ctx.send("waiting reaction for the message above")
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

        save(to_react,"to_react")
        pp.pprint(to_react)
        # react on the message
        cat = discord.utils.get(ctx.guild.channels, id=chan_id)

        await (await cat.fetch_message(id_msg)).add_reaction(reaction.emoji)

@bot.command(name='del-emoji-role')
async def del_emoji_role(ctx, id_msg : int, role):
    print("[del role emoji] ")
    def check(reaction, user):
        return user == ctx.author and reaction.message.id == ctx.message.id  # and str(reaction.emoji) == '👍'
    await ctx.send("waiting reaction for the message above")
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
            await ctx.send("this emoji is not register for this message")
            return
        new_list = [(rrole,type_) for rrole, type_ in to_react[id_msg][emoji] if role != rrole]
        for rrole, type_ in to_react[id_msg][emoji]:
            print(rrole,role, rrole != role)


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
        await ctx.send(f"role {role} deleted from emoji {reaction.emoji}")
        pp.pprint(to_react)
        save(to_react,"to_react")

### SET ROLE By DEFAULT ON SERVER JOIN

@bot.event #comment for now
async def on_member_join(member):
    print(f"Ajout du role Auth a {member.display_name}")
    #role = discord.utils.get(member.guild.roles, name="Auth")
    #await member.add_roles(role)


### CHANGE USER ROLE ON REACTIOn

@bot.event
async def on_raw_reaction_add(reactionPayload):
    msg_id = reactionPayload.message_id
    emoji_real = reactionPayload.emoji
    member = reactionPayload.member
    guild = member.guild
    emoji = emoji_get_id(emoji_real)
    print(emoji)
    #pprint(to_react)
    if msg_id in to_react.keys():
        # a = [elt for elt in to_react[msg_id].keys()]
        # a.append(emoji)
        # print(a)
        if emoji in to_react[msg_id].keys():
            for role_name, type_ in to_react[msg_id][emoji]:

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

@bot.event
async def on_raw_reaction_remove(reactionPayload):
    msg_id = reactionPayload.message_id
    emoji = emoji_get_id(reactionPayload.emoji)
    guild_id = reactionPayload.guild_id
    user_id = reactionPayload.user_id

    #guild = discord.utils.get(bot.guilds,id=guild_id)
    guild = bot.get_guild(guild_id)
    print("(------------------------------------)")
    print("nb members : " + str(len(guild.members)))
    for m in guild.members:
        print(m)
    member = discord.utils.get(guild.members,id=user_id)
    pp.pprint(guild)
    print(f"{guild.name} {member} <------- TEST")
    if msg_id in to_react.keys():
        if emoji in to_react[msg_id].keys():
            print("2")
            for role_name, type_ in to_react[msg_id][emoji]:
                print("3",role_name,type_)
                if type_ in [1, 3]:
                    await deleteRole(guild, member, role_name)


async def deleteRole(guild, member, role_name):
    pass
    print(f"delete the role {role_name} to {member.display_name}")
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        print(f"{role_name} n'hesite pas sur ce serveur")
    else:
        await member.remove_roles(role)


if(os.path.exists("to_react")):
    load("to_react")
bot.run(TOKEN)

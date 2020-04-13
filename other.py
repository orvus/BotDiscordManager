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
@bot.event
async def on_raw_reaction_add(reactionPayload):
    guild = reactionPayload.member.guild
    user = discord.utils.get(guild.members, id=reactionPayload.user_id)
    l = ["TICKET LOTERIE " + str(i) for i in range(1, 8)]
    if all(l) in [role.name for role in user.roles]:
        print(f"{user.name} a tous trouvé")

    chan = discord.utils.get(guild.channels, id= reactionPayload.channel_id)
    #msg = discord.utils.get(chan.messages, id=reactionPayload.message_id)
    msg = await chan.fetch_message(reactionPayload.message_id)

    role = discord.utils.get(guild.roles, name="Barman")
    here = reactionPayload.emoji
    reac = None
    for react in msg.reactions:
        if react.emoji == here.name:
            reac = react
    if chan.id == 693219559267762183 and msg.id == 693219654935773214:
        print(f"{here}")
        if here.name in ["🍻", "🍺", "🍷", "🍸"]:
            private_chan = await user.create_dm()
            await private_chan.send("voici ton verre",file=discord.File(f".\\plop.png"))
            print(f"test {here} - {reac.count}")
            if reac.count in [i for i in range(100, 1000, 100)]:
                await chan.send(f"{role.mention} il y a {reac.count} bières commandé, à toi de jouer")



bot.run(TOKEN)

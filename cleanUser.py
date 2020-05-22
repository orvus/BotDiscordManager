# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pickle
import pprint


pp = pprint.PrettyPrinter(indent=0)

load_dotenv(dotenv_path=".envTyo")

bot = commands.Bot(command_prefix='.')
###############################
# GLOBAL VARIABLE
###############################
TOKEN = os.getenv('DISCORD_TOKEN')


################
# BOT COMMAND  #
################
## GET STATE OF BOT ##
## ADD reaction roles ##




@bot.event
async def on_ready():
    print("bot online")


@bot.command(name='test')
async def test(ctx, state1):
    print("command ok")

@bot.command(name='delRole')
async def delRole(ctx, state1):
    print("del role")
    await ctx.send(f"Plus de {state1} sur le festival")

    #guild = ctx.guild
    #role1 = discord.utils.get(guild.roles, name=state1)
    #for member in guild.members:
    #   await ctx.send(f"{member.display_name} suppression du role")
    #   await member.remove_roles(role1)
    #
    #await ctx.send("Plus de {state1} sur le festival")

@bot.event
async def on_message(message):
    print(message.content)
    txt = message.content
    gandalf = "gandalf"
    i = 0
    for lettre in txt:
        if lettre == gandalf[i]:
            i += 1
        if i == len(gandalf):
            await message.channel.send(file=discord.File(".\\tenor.gif"), delete_after=10)
            return


#azgzraegnzrdzrgaazrlazgfgz
#gazandalaaaaz
bot.run(TOKEN)

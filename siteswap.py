# bot.py
import os
import subprocess
import asyncio
import random
import time
import discord
from discord.ext import commands
import copy
from dotenv import load_dotenv
import urllib.request
import hashlib
import wget

load_dotenv(dotenv_path=".env2")

global loop
loop = True

TOKEN = os.getenv('DISCORD_TOKEN_SITESWAP')
bot = commands.Bot(command_prefix='+')


@bot.command(name='siteswap', help="""Send a message with a siteswap and the bot will send you te gif if it exist\n
some example :\n
+siteswap 333
+siteswap (4,2x)(2x,4)
+siteswap [333]33
+siteswap <3p|3p><3|3><3|3><3|3>""")
async def siteswap(ctx, *,siteswap="333"):

    if ctx.channel.id not in [702470629198266388]:
        await ctx.message.delete(delay=1.0)
        print("pas le droit d'ecrire")
        return

    siteswap = siteswap.replace(" ", "")
    siteswapEnc = siteswap.encode()
    #ret = os.system(f"./JugglingLab/jlab.bat togif \"{siteswap}\" -out plop.gif")
    print(f" hash({siteswap}) = {hashlib.sha256(siteswapEnc).hexdigest() } ")
    if os.path.exists(f"./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif") is False:
        #result = subprocess.run([".\\JugglingLab\\jlab.bat", "togif", f"{siteswap}", "-out", f".\\Siteswap\\{hashlib.sha256(siteswapEnc).hexdigest()}.gif"])
        print(f"./JugglingLab/jlab togif \"pattern={siteswap}\" -prefs \"slowdown=2.9;fps=33.3\" -out ./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif")
        os.system(f"./JugglingLab/jlab togif \"pattern={siteswap}\" -prefs \"slowdown=2.9;fps=33.3\" -out ./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif")
        #print(f"{result.args}") -prefs \"width=280;height=320;slowdown=1.0;fps=33.3\"
        #print(f"{result.stderr} | {result.stdout} ")

    else:
        print("siteswap already exist")
    if(os.path.exists(f"./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif")):
        print("file exist")
        await ctx.send(content=f"{ctx.author.mention} voila le siteswap {siteswap} ", file=discord.File(f"./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif"))
    else:
        print("fail")

        await ctx.send(content=f"voila le siteswap {siteswap}",file=discord.File("./Siteswap/juggler.gif"), delete_after=10.0)
        await ctx.send(content=f"**OU PAS**, voici le lien de juggling lab pour apprendre le siteswap : https://jugglinglab.org/html/ssnotation.html ", delete_after=10.0)
    try:
        await ctx.message.delete(delay=1.0)
    except:
        print("no msg to del")
    await ctx.send(content=f"pour m'utiliser fait +siteswap <ton siteswap>\nexemple : +siteswap 441")
    #os.remove(f".\\Siteswap\\{hashlib.sha256(siteswapEnc).hexdigest()}.gif")

bot.run(TOKEN)



#"@gym siteswap généré alea ou list de siteswap compliqué"

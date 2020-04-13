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

list_siteswap=[
51,
423,
531,
450,
4413,
5313,
52413,
53142,
55113,
45051,

534,
5353,
6631,
6451,
55613,
56234,
56414,

5555,
6455,
6635,
97531,
771,
672,
645645,
663645,
666660,
663,
645,
63645,
75751,
88441
]

TOKEN = os.getenv('DISCORD_TOKEN_SITESWAP')
bot = commands.Bot(command_prefix='+')
@bot.command(name="launchDefi",help =" Admin command for siteswap challenge")
async def launch_defi(ctx, state="Start"):
    global loop
    if "Roboticien" not in [ role.name for role in ctx.author.roles]:
        return
    chan = discord.utils.get(ctx.guild.channels, id=695753675263705119)
    gym = discord.utils.get(ctx.guild.roles, name="GYM")
    i = 0
    if state == "Start":
        loop = True
        await ctx.send(content="start defi")
        while loop:
            i += 1
            siteswap = str(list_siteswap[i%len(list_siteswap)])
            siteswapEnc = siteswap.encode()
            os.system(f"./JugglingLab/jlab togif \"pattern={siteswap}\" -prefs \"slowdown=2.9;fps=33.3\" -out ./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif")
            await chan.send(content=f"** {gym.mention} Défi ! Peux-tu réussir ce siteswap ?\n{siteswap}**", file=discord.File(f"./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif"))
            #await chan.send(content=f"plop {list_siteswap[i]}")
            print("plop")
            time.sleep(3600)
    elif state == "End":
        await ctx.send(content="stop defi")
        loop = False
    print("ended")




@bot.command(name='siteswap', help="""Send a message with a siteswap and the bot will send you te gif if it exist\n
some example :\n
+siteswap 333
+siteswap (4,2x)(2x,4)
+siteswap [333]33
+siteswap <3p|3p><3|3><3|3><3|3>""")
async def siteswap(ctx, *,siteswap="333"):

    if ctx.channel.category.id not in [693208371083345980, 693217891788652604, 694240938196992090, 693212095243616407, 693272992683261953, 693211775239323679,693212218011025428 ]:
        await ctx.message.delete(delay=1.0)
        print("pas le droit d'ecrire")
        return

    siteswap = siteswap.replace(" ", "")
    siteswapEnc = siteswap.encode()
    #ret = os.system(f"./JugglingLab/jlab.bat togif \"{siteswap}\" -out plop.gif")
    print(f" hash({siteswap}) = {hashlib.sha256(siteswapEnc).hexdigest() } ")
    if os.path.exists(f".\\Siteswap\\{hashlib.sha256(siteswapEnc).hexdigest()}.gif") is False:
        #result = subprocess.run([".\\JugglingLab\\jlab.bat", "togif", f"{siteswap}", "-out", f".\\Siteswap\\{hashlib.sha256(siteswapEnc).hexdigest()}.gif"])
        print(f".\\JugglingLab\\jlab togif \"pattern={siteswap}\" -prefs \"slowdown=2.9;fps=33.3\" -out .\\Siteswap\\{hashlib.sha256(siteswapEnc).hexdigest()}.gif")
        os.system(f".\\JugglingLab\\jlab togif \"pattern={siteswap}\" -prefs \"slowdown=2.9;fps=33.3\" -out .\\Siteswap\\{hashlib.sha256(siteswapEnc).hexdigest()}.gif")
        #print(f"{result.args}") -prefs \"width=280;height=320;slowdown=1.0;fps=33.3\"
        #print(f"{result.stderr} | {result.stdout} ")

    else:
        print("siteswap already exist")
    if(os.path.exists(f"./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif")):
        print("file exist")
        await ctx.send(content=f"{ctx.author.mention} voila le siteswap {siteswap} ", file=discord.File(f".\\Siteswap\\{hashlib.sha256(siteswapEnc).hexdigest()}.gif"))
    else:
        print("fail")

        await ctx.send(content=f"voila le siteswap {siteswap}",file=discord.File(".\\Siteswap\\juggler.gif"), delete_after=10.0)
        await ctx.send(content=f"**OU PAS**, voici le lien de juggling lab pour apprendre le siteswap : https://jugglinglab.org/html/ssnotation.html ", delete_after=10.0)
    try:
        await ctx.message.delete(delay=1.0)
    except:
        print("no msg to del")
    #os.remove(f".\\Siteswap\\{hashlib.sha256(siteswapEnc).hexdigest()}.gif")


    #print(f"gif : {gif}")
    #if gif != None:
    #    await ctx.send(content=f"voila le siteswap {siteswap} ", file=discord.File(gif))
    #else:
    #    await ctx.send(content=f"voila le siteswap {siteswap}",file=discord.File("juggler.gif"))
    #    await ctx.send(content=f"**OU PAS**, voici le lien de juggling lab pour apprendre le siteswap : https://jugglinglab.org/html/ssnotation.html ")

bot.run(TOKEN)



#"@gym siteswap généré alea ou list de siteswap compliqué"

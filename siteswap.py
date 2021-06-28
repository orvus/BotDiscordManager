# bot.py
import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv
import hashlib


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
async def siteswap(ctx, *, siteswap = "333"):

    ## uncomment and put a chan id if you xant to limit the usage of the bot to one discord channel
    #if ctx.channel.id not in [702470629198266388]:
        #await ctx.message.delete(delay=1.0)
        #print("pas le droit d'ecrire")
        #return

    siteswap = siteswap.replace(" ", "")
    siteswapEnc = siteswap.encode()

    #the hash of the siteswap is use for known if it has already been search, generated and store
    print(f" hash({siteswap}) = {hashlib.sha256(siteswapEnc).hexdigest() } ")

    imagePath = Path(f"./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif")

    # if the siteswap has not been already use
    # use juggling lab for create GIF and store it for speed the next load
    if imagePath.exists() is False:
        cmd = Path("JugglingLab/jlab")
        arg1 = "togif"
        arg2 = f"\"pattern={siteswap}\""
        arg3 = "-prefs \"slowdown=2.9;fps=33.3\""
        arg4 = "-out " + str(imagePath)

        print(f"{cmd} {arg1} {arg2} {arg3} {arg4} ")
        os.system(f"{cmd} {arg1} {arg2} {arg3} {arg4}")
    #if the GIF is in local
    else:
        print("siteswap already exist")

    # at this moment, the image should exists, if not, it's a failure
    if imagePath.exists():
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

bot.run(TOKEN)

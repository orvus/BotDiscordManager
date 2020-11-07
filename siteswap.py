#!/usr/bin/env python3
# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import hashlib
from pathlib import Path

load_dotenv(dotenv_path=".env")
TOKEN = os.getenv('DISCORD_TOKEN_SITESWAP')
bot = commands.Bot(command_prefix='+')

exec_path = Path("./JugglingLab/jlab")
dir_img = Path("./Siteswap/")

fail_gif_path = Path("./Siteswap/juggler.gif")

@bot.command(name='siteswap', help="""Send a message with a siteswap and the bot will send you te gif if it exist\n
some example :\n
+siteswap 333
+siteswap (4,2x)(2x,4)
+siteswap [333]33
+siteswap <3p|3p><3|3><3|3><3|3>""")
async def siteswap(ctx, *,f_siteswap="333"):

    #### IF not in the good channel #####TODO not generic function for now
    #if ctx.channel.id not in [702470629198266388]:
    #    await ctx.message.delete(delay=1.0)
    #    print("pas le droit d'ecrire")
    #    return

    ##### parse input file ###### TODO gestion cas d'erreur
    f_siteswap = f_siteswap.replace(" ", "")

    ##### look the sha256 of the figure
    siteswapEnc = f_siteswap.encode()
    print(f" hash({siteswap}) = {hashlib.sha256(siteswapEnc).hexdigest() } ")
    print(dir_img / "{}.gif juggling : {}".format(hashlib.sha256(siteswapEnc).hexdigest(), f_siteswap))
    ##### look if the figure has been already computed
    if os.path.exists( dir_img / "{}.gif".format(hashlib.sha256(siteswapEnc).hexdigest())) is False:
        print(str(exec_path) + " togif \"pattern={}\" -prefs \"slowdown=2.9;fps=33.3\" -out ".format(f_siteswap) + str(dir_img / "{}.gif".format(hashlib.sha256(siteswapEnc).hexdigest())))
        os.system(str(exec_path) + " togif \"pattern={}\" -prefs \"slowdown=2.9;fps=33.3\" -out ".format(f_siteswap) + str(dir_img / "{}.gif".format(hashlib.sha256(siteswapEnc).hexdigest())))
        #os.system(f"./JugglingLab/jlab togif \"pattern={siteswap}\" -prefs \"slowdown=2.9;fps=33.3\" -out ./Siteswap/{hashlib.sha256(siteswapEnc).hexdigest()}.gif")
    else:
        print("siteswap already exist")
    if(os.path.exists( dir_img / "{}.gif".format(hashlib.sha256(siteswapEnc).hexdigest()))):
        print("file exist")
        await ctx.send(content=f"{ctx.author.mention} voila le siteswap {f_siteswap} ", file=discord.File(dir_img / "{}.gif".format(hashlib.sha256(siteswapEnc).hexdigest())))
    else:
        print("fail to load image")

        await ctx.send(content=f"voila le siteswap {f_siteswap}",file=discord.File(fail_gif_path), delete_after=10.0)
        await ctx.send(content=f"**OU PAS**, voici le lien de juggling lab pour apprendre le siteswap : https://jugglinglab.org/html/ssnotation.html ", delete_after=10.0)
    try:
        await ctx.message.delete(delay=1.0)
    except:
        print("no msg to del")
    await ctx.send(content=f"pour m'utiliser fait +siteswap <ton siteswap>\nexemple : +siteswap 441")

bot.run(TOKEN)
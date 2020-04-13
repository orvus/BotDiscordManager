# bot.py
import os
import asyncio
import random
import time
import discord
from discord.ext import commands
import copy
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

###############################
# GLOBAL VARIABLE
###############################
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')
subscribChan = dict()
#structure
#   sub[id chan d'ecoute] = [chan d'ecriture de texte pour visio]
createdChan = dict()
#structure
#   sub[id chan crée] = [message visio,chief,name_pattern]
pendingUser = []
pendingUser2 = dict()


####
# SPECIAL sentance for some place
####
phrase = dict()
phrase[692032285473505282] = ["Voiture de {}", "Caisse de {}", "Van de {}"] # PARKING
phrase[692062516615970906] = ["Tatami de {}", "Coin de {}", "Tapis de sol de {}"] # GYMNASE
#phrase[691815688632795187] = [] # CHAPITEAUX
phrase[691717153241563206] = ["🍺 Table de {} 🍺", "🍻 Table de {} 🍻", "🍸 Table de {} 🍹", "🍷 Table de {} 🍺"] # BUVETTE


### v1
phrase = dict()
phrase[693244728002478200] = ["Tatami de {}", "Coin de {}", "Tapis de sol de {}"] # GYMNASE
#phrase[691815688632795187] = [] # CHAPITEAUX
phrase[693219796531019816] = ["🍺 Table de {} 🍺", "🍻 Table de {} 🍻", "🍸 Table de {} 🍹", "🍷 Table de {} 🍺"] # BUVETTE
phrase[693212825614680114] = ["Tente de {}"] # CAMPING
phrase[693940012642992228] = ["Workshop de {}"] # workshop (cat id 693243443618644048)

wsCatId=693243443618644048
################################
################################
################################


######## UTILS FUNCTION #############
def chooseChanName(forkChan_id):
    if forkChan_id in phrase.keys():
        return random.choice(phrase[int(forkChan_id)])
    else:
        return "Espace de {}"

def _writeEnv():
    with open(".env", "w+") as f:
        f.seek(0)
        f.truncate(0)
        f.write(f"DISCORD_TOKEN={TOKEN}")
        f.write("\n")
        f.write(f"DISCORD_NB_LINK={len(subscribChan.keys())}")
        f.write("\n")
        i = 0
        for key, value in subscribChan.items():
            f.write(f"DISCORD_LINK_VOICE_{i}={key}\n")
            f.write(f"DISCORD_LINK_TEXT_{i}={value}\n")
            i += 1
def _loadEnv():
    print("LOAD :")
    dic_size = os.getenv("DISCORD_NB_LINK")
    if dic_size is not None:
        for i in range(int(dic_size)):
            tmp_key = os.getenv(f"DISCORD_LINK_VOICE_{i}")
            tmp_value = os.getenv(f"DISCORD_LINK_TEXT_{i}")
            subscribChan[int(tmp_key)] = int(tmp_value)
            print(tmp_key,tmp_value)

def getChanFromId(guild,_id):
    return discord.utils.get(guild.channels, id=int(_id))
def getUserFromId(guild,_id):
    return discord.utils.get(guild.members, id=int(_id))
#######################################



################
# BOT COMMAND  #
################
## GET STATE OF BOT ##
@bot.command(name = "event", help = "fonction passive du bot:\r\n\
\t(codé/à tester) ajout du rôle 'to early' au nouveau arrivant\n\
\t(future) substitution a reation roles\r\n\
\t(future) autre améliorations pas encore pensées")
async def eventhelper(ctx):
    response = "channel ecouté :\n"
    for k, v in subscribChan.items():
        #print("sub",v)
        response += f"+ vocal : {getChanFromId(ctx.guild,k)} text chan : {getChanFromId(ctx.guild,v)}\n"
    for k, v in createdChan.items():
        #print("creat",v)
        response += f"- created : {getChanFromId(ctx.guild, k)} message : {v['msg'].content}\n"
    await ctx.send(response)



## ADD DISPATCHER CHANNEL ##
@bot.command(name='add-dispatcher-channel',help="Crée un nouveaux canal d'écoute\n argument : \n <identifiant du canal a ecouter>  <identifiant du canal ou le lien de la visio sera posté>" )
async def add_dispatcher_channel(ctx, channel_id=0, channel_txt_id=0):
    print("add dispatcher")
    guild = ctx.guild
    #for gc in guild.channels:
    #    print(gc.name," - ",gc.id)
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))

    if not existing_channel:
        print("channel doesn't exist")
    else:
        #for c in guild.channels:
        #    print(f"{c.id} | {c.name}")
        #print(f"{discord.utils.get(guild.channels, id=int(channel_id))}")
        print(f"on enregistre le chan dispatcher : {channel_id} ({getChanFromId(guild,channel_id)})et le txt {channel_txt_id} ({getChanFromId(guild,channel_txt_id)})")
        subscribChan[channel_id] = channel_txt_id
        _writeEnv()

## PENDING USER AFTER LEAVE CHAN ## TODO 2?
async def pending(user):
    pendingUser.append(user)
    #time.sleep(1)
    pendingUser.remove(user)
async def pending2(user):
    pendingUser.append(user)
    time.sleep(1)
    pendingUser.remove(user)

##############################################
#                EVENT BOT                   #
##############################################

## ADD REATION ON PEOPLE  WHEN ENTERING IN SERVER ##
@bot.event
async def on_member_join(member):
    guild = member.guild
    roles = guild.roles
    role_to_give = discord.utils.get(roles, name="Arrivant")
    print(f"on ajoute le role {role_to_give} a {member.name}")
    if role_to_give is not None:
        await member.add_roles(role_to_give)

## CHANGE VOICE STATUS ##
# use for :
#   go on dispatcher chan
#   leave created chan
#       need to suppress it ?
#       did he leaved his chan ? y : rename it
@bot.event
async def on_member_update(before, after):
    roleUsed="Perdu"
    if before is not None and after is not None:
        bef = [role.name for role in before.roles]
        aft = [role.name for role in after.roles]
        #print(bef, aft)
        if roleUsed not in bef and roleUsed in aft:
            print(f"roles {roleUsed} added to {after.name}")
            ## il faut recupérer le serveur discord
            chan = discord.utils.get(after.guild.channels, id=693197540228595762)
            await after.move_to(chan)



def isEnglish(member):
    eng = "English-speaking"
    roles = [role.name for role in member.roles]
    if eng in roles:
        return True
    return False


@bot.event
async def on_voice_state_update(member, before, after):
    before = copy.copy(before)
    after = copy.copy(after)

    #await cleanUnused(member.guild) #??
    i = random.randint(0, 1000)
    print(f"{i}changement de status pour : {member.name} {time.time()}")

    #####
    # before != after
    ####
    if before is not None and before.channel is not None and after is not None and after.channel is not None and\
            before.channel.id == after.channel.id:
        print("-don't care about this voice event")
        return # leave because we don't care about thoses event

######################################
#         LEAVE CHAN CREATED         #
######################################

    if before is not None and before.channel is not None and before.channel.id in createdChan.keys():
        print(f"-quitte un canal vocal crée par le bot")
        asyncio.create_task(pending(member.name))
        #
        if len(before.channel.members) == 0 or \
                (createdChan[before.channel.id]['chief_id'] == member.id and before.channel.category_id == wsCatId):
            if (createdChan[before.channel.id]['chief_id'] == member.id and before.channel.category_id == wsCatId):
                #delete chan txt
                print("created chan to delete intervenant : ", createdChan[before.channel.id])
                txt_id = createdChan[before.channel.id]["txt_id"]
                chan_txt = None
                for txt_chan in member.guild.text_channels:
                    if txt_chan.id == txt_id:
                        chan_txt = txt_chan

                if chan_txt is not None:
                    #chan_txt = discord.utils(member.guild.text_channels, id=txt_id)
                    try:
                        if chan_txt is not None:
                           await chan_txt.delete()
                    except:
                        print("--fail to delete chan text")
                else:
                    print("chan txt don't exist for this intervenant")


            print("--canal quitter devient vide, suppresion en cours")
            msg = createdChan[before.channel.id]["msg"]
            # pop elt from dico
            createdChan.pop(before.channel.id)
            try:
                await before.channel.delete()
            except:
                print("--fail to delete chan video")
            try:
                if msg is not None:
                    await msg.delete()
            except:
                print("--fail to delete text")


        elif createdChan[before.channel.id]['chief_id'] == member.id: # he leave but some people are always here
            print("--canal quitter non vide mais le gerant est partie")
            #if it is his chan : rename it
            guild = before.channel.guild
            chan = before.channel

            print(f"--have to change chief : {getUserFromId(guild, createdChan[before.channel.id]['chief_id'])} to {before.channel.members[0]}")
            print("--il y a dans le canal :")
            for user in before.channel.members:
                print(f"---{user.name}")
            # change chief channel
            createdChan[before.channel.id]['chief_id'] = before.channel.members[0].id

            # choose new name
            chief = getUserFromId(guild, createdChan[before.channel.id]['chief_id'])
            name = chief.nick
            if not chief.nick:
                name = chief.name

            await before.channel.edit(name=createdChan[before.channel.id]["name_pattern"].format(name))
            msg = createdChan[before.channel.id]["msg"]

            #await msg.edit(content=f"{getUserFromId(guild, createdChan[before.channel.id]['chief_id']).mention} here you can find your visio link : https://discordapp.com/channels/{guild.id}/{chan.id}")
            cont = f"Voilà le lien pour la visio {getUserFromId(guild, createdChan[before.channel.id]['chief_id']).mention} 🎬 https://discordapp.com/channels/{guild.id}/{chan.id} 🎬\n Hasta la vista Baby 💥"
            if isEnglish(member):
                cont = f"Here, the link of {getUserFromId(guild, createdChan[before.channel.id]['chief_id']).mention}'s viso 🎬 https://discordapp.com/channels/{guild.id}/{chan.id} 🎬\n Hasta la vista Baby 💥"
            await msg.edit(content=cont)


################## JUST FOR LOG #################
    if after is not None and after.channel is not None and after.channel.id in createdChan.keys():
        print(f"-arrive dans un channel crée par le bot : {after.channel.name}")
##################################################

###########################################
#         CREATION NOUVEAU CHAN           #
###########################################
    if after is not None and after.channel is not None and after.channel.id in subscribChan.keys():
        print(f"{i}il arrive dans : {after.channel.name}")
        if member.name in pendingUser: #please wait ###### NEVER COME HERE DU TO PENDING IMPLEMENTATION
            print("pending")
            await member.create_dm()
            await member.dm_channel.send(
                f'Please wait a least 5 seconds before making an other channel'
            )
        else: # ok make new channel

            if after.channel.id not in subscribChan.keys():
                print("error num 1")
            else:
                guild = after.channel.guild
                name = member.display_name
                # creation of the chat name
                channel_name_pattern = chooseChanName(after.channel.id)
                channel_name = channel_name_pattern.format(name)

                msg_txt = "Voilà le lien pour la visio {} 🎬 https://discordapp.com/channels/{}/{} 🎬\n Hasta la vista Baby 💥"
                if isEnglish(member):
                    msg_txt = "Here, the link of {}'s visio 🎬 https://discordapp.com/channels/{}/{} 🎬\n Hasta la vista Baby 💥"
                cat = discord.utils.get(guild.categories, id=after.channel.category_id)
                ############### INTERVENANT WS ############
                roles = [role.name for role in member.roles]
                if after.channel.category_id == wsCatId:
                    if "Intervenant.e" not in roles:
                        if before is not None and before.channel is not None:
                            try:
                                await member.move_to(before.channel)
                            except:
                                await member.move_to(None)
                        else:
                            await member.move_to(None)
                        return
                    else:
                        # creation de channel text
                        channel_text_name = f"🦋❓ws {name}"

                        #
                        msg_txt = "Vidéo link to see {}'s workshop 🎬 https://discordapp.com/channels/{}/{} . "
                ############################################

                print(f"{i}-make new chan")

                # channel_name += f"--{i}--"#debug#
                #
                #########################

                # creation of the new voice channel
                print(f"+{i}creation du nouveau salon {channel_name}")
                await guild.create_voice_channel(channel_name, category=cat)
                # get id of the new channel
                chan = discord.utils.get(guild.channels, name=channel_name)
                print(f"+{i}creation du nouveau salon id :{chan.id}")
                # get text chan for write message to user
                chan_txt_id = subscribChan[after.channel.id]
                chan_txt = discord.utils.get(guild.channels, id=chan_txt_id)

                #write message to user
                #msg = await chan_txt.send(f"{member.mention} here you can find your visio link : https://discordapp.com/channels/{guild.id}/{chan.id}")
                msg = await chan_txt.send(msg_txt.format(member.mention, guild.id, chan.id))
                await msg.edit(suppress=True)
                print(f"+{i} ecriture du msg ok")

                #update python struct
                print(f"+{i}going to update python")
                createdChan[chan.id] = {"msg": msg, "chief_id": member.id, "name_pattern": channel_name_pattern} # init
                print(f"+{i}update python ok")

                #move user to the new chan
                await member.move_to(chan)
                if after.channel.category_id == wsCatId and "Intervenant.e" in roles:
                    txt_chan = await guild.create_text_channel(channel_text_name, category=cat)
                    createdChan[chan.id] = {"msg": msg, "chief_id": member.id, "name_pattern": channel_name_pattern, "txt_id": txt_chan.id} # init
                print(f"+{i} fin {time.time()}")


# ################## SAFTY ######################
async def cleanUnused(guild):
    print("clean unused chan")
    for chan_id in createdChan.keys():
        chan = discord.utils.get(guild.channels, id=chan_id)
        if chan is not None:
            if len(chan.members) == 0:
                msg = createdChan[chan_id]

                # pop elt from dico
                createdChan.pop(chan_id)
                try:
                    await chan.delete()
                    await msg.delete()
                except:
                    print("fail to delete chan (video or txt)")

_loadEnv()

bot.run(TOKEN)

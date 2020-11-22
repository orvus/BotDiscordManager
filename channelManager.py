#!/usr/bin/env python3
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from utils import *


load_dotenv(dotenv_path=".env")
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
# command *
bot = commands.Bot(command_prefix='*')


#######################
### UTILS CHAN INFO ###
#######################


def allocate_new_guild(guild_id):
    g_guild_tab[guild_id] = {"fork": dict(), "created": dict(), "default_param": default_param}

def chooseChanName(g,chan_id):
    try:
        print(g_guild_tab[g.id]["fork"][chan_id])
        if g_guild_tab[g.id]["fork"][chan_id]["childs_names_list"] != []:
            return random.choice(g_guild_tab[g.id]["fork"][chan_id]["childs_names_list"])
    except:
        print("ALX NOP")
        pass
    try:
        return g_guild_tab[g.id]["default_param"]["chan_name"]
    except:
        return default_param["chan_name"]

def is_valid_chan_name(s, nb):
    cnt = 0
    prev = False
    for c in s:
        if prev is False and c == "{":
            prev = True
            continue
        if prev is True and c == "}":
            cnt += 1
        else:
            prev = False
    return cnt == nb

def is_chan_in_forkeur(guild, chan):
    try:
        if chan is None:
            return False
        if chan.id in g_guild_tab[guild.id]["fork"]:
            return True
        else:
            return False
    except:
        return False


def is_chan_in_created(guild, chan):
    try:
        if chan is None:
            return False
        if chan.id in g_guild_tab[guild.id]["created"]:
            return True
        else:
            return False
    except:
        return False
######################
####  GOBAL INFO  ####
######################
g_guild_tab = dict()
# id chan
#   int : id chan txt link
#   bool: creat chan txt ?
#   int : nb phrases pattern
#   phrases[
#       str = "... {} ..."]
#  {"txt_chan_id": channel_txt_id, "child_chan_txt": False, "nb_phrase_pattern": 0, "role": None}

# id chan created
#   int : msg_id
#   int : id creator
#   str : phrase pattern used
#   int : id txt (None

default_param = {"chan_name": "Espace de {}",
                 "archive": "archive"
                 }


###############
# BOT COMMAND #
###############

@bot.command(name='canal-de-dispersion',
             help="Crée un nouveaux canal d'écoute\n argument : \n <identifiant du canal a ecouter> " )
async def add_dispatcher_channel(ctx, channel_id: int):
    guild = ctx.guild
    if guild.id not in g_guild_tab.keys():
        allocate_new_guild(guild.id)
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist")
        await ctx.send("erreur ajout canal (cannal inexistant)")
    elif channel_id in g_guild_tab[guild.id]["fork"]:
        print("erreur ajout canal (canal vocal  deja ajouté")
        await ctx.send("erreur ajout canal (cannal vocal deja ajouté)")
    else:
        print(f"on enregistre le chan dispatcher : {channel_id} ({getChanFromId(guild,channel_id)} ")
        g_guild_tab[guild.id]["fork"][channel_id] = {"child_chan_txt": False,
                                                   "nb_name_pattern": 0,
                                                   "childs_names_list": [],
                                                   "role": [],
                                                   "del_on_leave": False
                                                   }
        save(g_guild_tab,"g_guild_tab")
        await ctx.send("canal ajouté")

@bot.command(name='canal-de-dispersion-supr',
             help="Supprime un canal d'écoute\n argument : \n <identifiant du canal a supprimer>  ")
async def del_dispatcher_channel(ctx, channel_id: int):
    print("del fork chan")
    guild = ctx.guild
    if guild.id not in g_guild_tab.keys():
        await ctx.send("Aucune information sur le serveur de trouvée, commande ignorée")
        return

    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if existing_channel is None or channel_id not in g_guild_tab[guild.id]["fork"].keys():
        print("channel doesn't exist or not register")
        await ctx.send("Erreur suppression canal (n'existe pas ou n'est pas enregisté)")
    else:
        print(f"on supprime le chan dispatcher : {channel_id} ({getChanFromId(guild,channel_id)})")
        del g_guild_tab[guild.id]["fork"][channel_id]
        save(g_guild_tab,"g_guild_tab")
        await ctx.send("canal supprimé")

@bot.command(name='canal-de-dispersion-nom-ajout',
             help="Ajoute un nom de canal possible pour les cannaux crée par les cannaux de **canal-de-dispersion**")
async def add_named_chan(ctx, channel_id : int, *remain):
    print(f"add sentence for {channel_id}")
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist or not register")
        await ctx.send(f"le canal {existing_channel.name if existing_channel is not None else existing_channel} n'est pas enregistré dans les canaux d'écoute")
        return

    if guild.id not in g_guild_tab.keys():
        allocate_new_guild(guild.id)

    if channel_id not in g_guild_tab[guild.id]["fork"].keys():
        await add_dispatcher_channel(ctx, channel_id)

    g_guild_tab[guild.id]["fork"][channel_id]["nb_name_pattern"] += len([r for r in remain if is_valid_chan_name(r, 1)])
    if "childs_names_list" not in g_guild_tab[guild.id]["fork"][channel_id].keys():
        g_guild_tab[guild.id]["fork"][channel_id]["childs_names_list"] = list()
    g_guild_tab[guild.id]["fork"][channel_id]["childs_names_list"].extend([r for r in remain if is_valid_chan_name(r, 1)])
    save(g_guild_tab,"g_guild_tab")
    await ctx.send(f"Noms ajoutés sauf : {[r for r in remain if not is_valid_chan_name(r, 1)]}")

@bot.command(name='canal-de-dispersion-nom-supr',
             help="Supprime un nom de canal possible pour les cannaux crée par les cannaux de **canal-de-dispersion**")
async def del_named_chan(ctx, channel_id : int, *to_del):
    print(f"del sentence for {channel_id}")
    guild = ctx.guild
    if guild.id not in g_guild_tab.keys():
        await ctx.send("Aucune information trouvé")
        return

    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if existing_channel is None or channel_id not in g_guild_tab[guild.id]["fork"].keys():
        print("channel doesn't exist")
        await ctx.send("erreur suppression texte")
    else:
        for elt in [r for r in to_del]:
            print(elt, g_guild_tab[guild.id]["fork"][channel_id]["childs_names_list"])
            if elt in g_guild_tab[guild.id]["fork"][channel_id]["childs_names_list"]:
                g_guild_tab[guild.id]["fork"][channel_id]["nb_name_pattern"] -= 1
                g_guild_tab[guild.id]["fork"][channel_id]["phrases"].remove(elt)
        save(g_guild_tab,"g_guild_tab")
        await ctx.send("textes supprimé")


@bot.command(name='canal-de-role-ajout',
             help="Seul les personnes possedant ces role pourront ouvrir des canaux  **add-fork-chan**")
async def add_role_chan(ctx, channel_id: int, *to_add):
    print(f"add role for {channel_id}")
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist")
        await ctx.send("erreur ajout roles (canal n'existe pas)")
        return

    if guild.id not in g_guild_tab.keys():
        allocate_new_guild(guild.id)

    if channel_id not in g_guild_tab[guild.id]["fork"].keys():
        await add_dispatcher_channel(ctx, channel_id)


    guild_roles = get_values(guild, "roles", "name")
    print(to_add, guild_roles, g_guild_tab[guild.id]["fork"][channel_id]["role"])
    g_guild_tab[guild.id]["fork"][channel_id]["role"].extend([r for r in to_add if r in guild_roles and r not in g_guild_tab[guild.id]["fork"][channel_id]["role"]])
    print(f"les roles autorisé : {g_guild_tab[guild.id]['fork'][channel_id]['role']}")
    save(g_guild_tab,"g_guild_tab")
    await ctx.send(f"roles autorisé : {g_guild_tab[guild.id]['fork'][channel_id]['role']}")

@bot.command(name='canal-de-role-supr',
             help="Supprime les roles des accès a ce chan")
async def del_role_chan(ctx, channel_id: int, *remain):
    print(f"del role for {channel_id}")
    guild = ctx.guild
    if guild.id not in g_guild_tab.keys():
        await ctx.send("Aucune information trouvé")
        return
    existing_channel = getChanFromId(guild, channel_id)
    if not existing_channel and channel_id not in g_guild_tab[guild.id]["fork"].keys():
        print("channel doesn't exist or not register")
        await ctx.send("erreur suppression roles (le canal n'existe pas ou n'est pas enregistré")
    else:
        for role in remain:
            try:
                g_guild_tab[guild.id]["fork"][channel_id]["role"].remove(role)
            except:
                print("role not in list")
        save(g_guild_tab,"g_guild_tab")
        await ctx.send("roles supprimés")


@bot.command(name='canal-txt-pour-canal-cree',
             help="Modifie le gestion des chan txt créent par les chan fils")
async def set_txt_creation_for_child(ctx, channel_id: int, is_txt: bool, is_archive: bool):
    print(f"modify  {channel_id} child txt creation")
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist")
        await ctx.send("erreur dans l'ajout de chan txt des chan crée")
        return

    if guild.id not in g_guild_tab.keys():
        allocate_new_guild(guild.id)

    if channel_id not in g_guild_tab[guild.id]["fork"].keys():
        await add_dispatcher_channel(ctx, channel_id)

    g_guild_tab[guild.id]["fork"][channel_id]["child_chan_txt"] = is_txt
    g_guild_tab[guild.id]["fork"][channel_id]["child_txt_archive"] = is_archive
    save(g_guild_tab,"g_guild_tab")
    await ctx.send(f"les chan créent par {getChanFromId(guild,channel_id)}   { 'auront' if is_txt else 'n auront pas' } de chan txt de crée et ils {'seront' if is_archive else 'ne seront pas'} archivés" )


@bot.command(name='canal-suppression-createur-quitte',
             help="modifie le gestion des chan txt créent par les chan fils")
async def del_on_leave(ctx, channel_id: int, to_del: bool, delay=0):
    print(f"modify  {channel_id}  (del on leave)")
    guild = ctx.guild
    if guild.id not in g_guild_tab.keys():
        print("make chan before use this function")
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel and channel_id not in g_guild_tab[guild.id]["fork"].keys():
        print("channel doesn't exist")
        await ctx.send("le chan n'est pas enregistré dans le bot")
    else:
        g_guild_tab[guild.id]["fork"][channel_id]["del_on_leave"] = to_del
        g_guild_tab[guild.id]["fork"][channel_id]["delay"] = delay
        save(g_guild_tab,"g_guild_tab")
        await ctx.send("mise a jour ok")


# ####### ############# ####### #
# ####### DEFAULT PARAM ####### #
# ####### ############# ####### #
@bot.command(name='change-default-chan-name',
             help="modifie le nom par défaut des chans crée")
async def set_default_name_to_child(ctx, name="Espace de {}"):
    guild = ctx.guild
    if guild.id not in g_guild_tab.keys():
        allocate_new_guild(guild)
    if is_valid_chan_name(name, 1):
        g_guild_tab[guild.id]["default_param"]["chan_name"] = name
        await ctx.send("nom par défaut changé")
    else:
        await ctx.send("il faut que le nom par defaut contiene au moins un '{}' pour etre valide")

@bot.command(name='set-archive-category',
             help="Modifie la catégorie servant a archivé les salons textuels")
async def set_default_archive(ctx, arch_id : int):
    guild = ctx.guild
    if guild.id not in g_guild_tab.keys():
        allocate_new_guild(guild.id)
    cat = discord.utils.get(guild.categories, id=arch_id)
    if cat is None:
        await ctx.send("cette categorie n'existe pas")
        return
    g_guild_tab[guild.id]["default_param"]["archive_id"] = arch_id
    await ctx.send("dossier d'archivage par defaut changé")


@bot.command(name="clean-created")
async def clean_created(ctx):
    if ctx.guild.id in g_guild_tab.keys():
        g_guild_tab[ctx.guild.id]["created"] = dict()
    save(g_guild_tab,"g_guild_tab")


@bot.command(name="clean-all")
async def clean_all(ctx):
    if ctx.guild.id in g_guild_tab.keys():
        g_guild_tab[ctx.guild.id]["fork"] = dict()
        g_guild_tab[ctx.guild.id]["created"] = dict()
        g_guild_tab[ctx.guild.id]["default_param"] = dict()
    save(g_guild_tab,"g_guild_tab")

##############################################
#                EVENT BOT                   #
##############################################

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    # UNUSEFULL event
    if before is not None and before.channel is not None and after is not None and after.channel is not None and\
            before.channel.id == after.channel.id:
        print("-don't care about this voice event")
        return # leave because we don't care about thoses event

    if is_chan_in_forkeur(guild, after.channel):
        print("after in forkeur chan")


        #si la personne qui veut créer un canal en a deja un old_chan sera non vide
        old_chan = [k for k, elt in g_guild_tab[guild.id]["created"].items() if elt["creator"] == member.id and elt["parent"] == after.channel.id]

        if len(old_chan) != 0:
            # TODO si le chan n'existe pas, le suprimer de la structure avant de continuer
            print("il possède deja un chan")
            await member.move_to(getChanFromId(guild, old_chan[0]))
            return

        channel_info = g_guild_tab[guild.id]["fork"][after.channel.id]
        member_role = get_values(member, "roles", "name")  # list(map(lambda role: role.name, member.roles))
        name = member.display_name
        channel_name_pattern = chooseChanName(guild, after.channel.id)
        print(channel_name_pattern)
        channel_name = channel_name_pattern.format(name)
        #print("creation du canal :" + channel_name + " text will be " + g_guild_tab[guild.id]["fork"][after.channel.id]["msg_txt"])
        print(f"user role {member_role} , {channel_info['role']}, {len(channel_info['role']) }")

        # Si le chan ne demmande aucun role ou si le membre possède le role d'ouverture du canal
        if len(channel_info["role"]) == 0 or contain_any(member_role, channel_info["role"]):
            print("check roles : ok")
            cat = discord.utils.get(guild.categories, id=after.channel.category_id)
            created_chan = await guild.create_voice_channel(channel_name, category=cat)
            g_guild_tab[guild.id]["created"][created_chan.id] = dict()
            g_guild_tab[guild.id]["created"][created_chan.id]["parent"] = after.channel.id
            g_guild_tab[guild.id]["created"][created_chan.id]["creator"] = member.id
            g_guild_tab[guild.id]["created"][created_chan.id]["title"] = channel_name_pattern
            await member.move_to(created_chan)

            if "child_chan_txt" in channel_info.keys():
                if channel_info["child_chan_txt"] is True:
                    txt_created_chan = await guild.create_text_channel(channel_name, category=cat)
                    g_guild_tab[guild.id]["created"][created_chan.id]["perso_txt_chan_id"] = txt_created_chan.id

        else:
            print("role not ok : leave")
            #TODO if connected before, go to before chan
            await member.move_to(None)

    if is_chan_in_created(guild, before.channel):
        print("before in created chan")
        parent_id = g_guild_tab[guild.id]["created"][before.channel.id]["parent"]
        # print(parent_id, guild_tab[guild.id]["fork"].values())
        if parent_id not in g_guild_tab[guild.id]["fork"].keys():
            print("bug, value changed ...")
            return

        parent_info = g_guild_tab[guild.id]["fork"][parent_id]
        current_info = g_guild_tab[guild.id]["created"][before.channel.id]
        #print(parent_info)
        #print(current_info)
        to_del = False
        if "del_on_leave" in parent_info.keys():
            to_del = parent_info["del_on_leave"]
        print("ok 1")
        #if len(before.channel.members) == 0 or (to_del is True and member.id == current_info["creator"]):

        # si la chan est vide ou que le chan s'autodetruit lorsque le createur part
        if len(before.channel.members) == 0 or (to_del is True and current_info["creator"] not in get_values(before.channel, "members", "id")):

            print(f"del voice chan ")
            if "delay" in parent_info.keys():
                print(f"wait {parent_info['delay']} seconds")
                await asyncio.sleep(parent_info['delay']) #TODO bug si l'auteur part revient et repart avant la fin du premier timer
                #si après x seondes, le proprio n'est pas revenue dans le chan, ne pas del le chan
                if current_info["creator"] in get_values(before.channel, "members", "id"):
                    print("still in")
                    return
            try:
                await before.channel.delete()
            except:
                print("skip delete chan voice")
            if "perso_txt_chan_id" in current_info.keys():  # it have to delete chan txt perso
                print("child have chan txt")
                if parent_info["child_txt_archive"] is True: # NO archive it

                    print(f"make archive later {discord.utils.get(guild.categories, name='archive')}")
                    print(f"cat name : {get_values(guild,'categories','name')}")
                    chan = getChanFromId(guild, current_info["perso_txt_chan_id"])
                    await chan.edit(
                        name=chan.name,
                        topic=chan.topic,
                        position=0,
                        sync_permissions=True,
                        category=discord.utils.get(guild.categories, name="________📚BIBLIOTHEQUE📚_________") #TODO hardcode
                    )
                    pass  # move chan txt to saved zone
                else: # delete chan txt of child
                    print("del chan txt")
                    try:
                        await getChanFromId(guild, current_info["perso_txt_chan_id"]).delete()  # change this later
                    except:
                        print("skip delete chan")
            try :
                del g_guild_tab[guild.id]["created"][before.channel.id]
                print(" python struct del ok")
            except :
                print("skip python struct del")
        #si le canal ne doit pas ce detruire quand le createur part
        elif to_del is False and member.id == current_info["creator"]:
            # choisi un nouveau créateur et renome le canal
            print("leave chan and i'm the creator")
            new_creator = before.channel.members[0].id # TODO choisir aleatoirement
            print(f"new creator is {getUserFromId(guild, new_creator).display_name }")
            current_info["creator"] = new_creator  # getUserFromId(guild, new_creator).display_name
            chan_name = g_guild_tab[guild.id]["created"][before.channel.id]["title"].format(getUserFromId(guild, current_info["creator"]).display_name)
            print(f"new chan name : {chan_name}")
            await before.channel.edit(name=chan_name)

    save(g_guild_tab,"g_guild_tab")
@bot.event
async def on_ready():
    print("bot online")
if(os.path.exists("g_guild_tab")):
    g_guild_tab = load("g_guild_tab")

bot.run(TOKEN)

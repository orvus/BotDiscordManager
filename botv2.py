# bot.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pickle
import pprint
import asyncio

pp = pprint.PrettyPrinter(indent=0)

load_dotenv(dotenv_path=".env")

###############################
# GLOBAL VARIABLE
###############################
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='£')
@bot.command(name='replique')
async def replique(ctx):
    await ctx.send(content="hasta la vista baby", tts=True)


@bot.command(name="chan-info")
async def chan_info(ctx, raw=""):

    embed = discord.Embed(
        color=discord.Colour.orange()
    )
    if ctx.guild.id not in guild_tab.keys():
        ret = "ce serveur n'a jamais grée de chan d'écoute"
        _name = f"{ctx.guild.name}"
        embed.add_field(name=_name,
                        value=ret,
                        inline=False)

    else:
        pp.pprint(guild_tab[ctx.guild.id])
        if raw == "raw":
            await ctx.send(pp.pformat(guild_tab[ctx.guild.id]))
            return

        for k, v in guild_tab[ctx.guild.id]["fork"].items():
            ret = ""
            _name = "Audio "+getChanFromId(ctx.guild, k).name

            # id du chan ou le fils ecrit son text
            if "txt_chan_id" in v.keys():
                if v["txt_chan_id"] != 0:
                    ret += f"lié avec {getChanFromId(ctx.guild, v['txt_chan_id']).name} \n"
                else:
                    ret += f" lié a aucun canal texte\n"
            # pattern du message que le fils utilise pour la visio
            if "msg_txt" in v.keys() and v["txt_chan_id"] != 0:
                ret += f"le message sera : {v['msg_txt']} \n"
            # le fils crée un chan txt ?
            if "child_chan_txt" in v.keys():
                ret += f"fils chan txt creation : {str(v['child_chan_txt']) }\n"
                # le chan txt sera sauvegarder ?
                if "child_txt_archive" in v.keys():
                    ret += f"archivage du chan textuel des fils  : {str(v['child_txt_archive'])}\n"
            # nom de titre possible pour le salon fils
            if "nb_phrase_pattern" in v.keys():
                ret += f"il y a {v['nb_phrase_pattern']} phrases\n"
            # nom possible pour les salon fils
            if "phrases" in v.keys():
                ret += f"les phrases sont : {v['phrases']}\n"
            # suppression du canal quand le createur part ?
            if "del_on_leave" in v.keys():
                ret += f"suppression sur depart : {v['del_on_leave']}\n"
            # role nécessaire pour ouvir le un chan fils
            if "role" in v.keys():
                if len(v["role"]) != 0:
                    ret += f"les role pouvant ouvrir des cannal {v['role']}\n"
                else:
                    ret += f"tous le monde peut créer des canaux\n"

            embed.add_field(name=_name,
                            value=ret,
                            inline=False)

    embed.set_author(name=bot.user.display_name)
    await ctx.send(embed=embed)

guild_tab = dict()
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


################################
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]


def save(var):
    print((namestr(var, globals())[0]))
    with open(namestr(var, globals())[0], "wb+") as f:
        print(f)
        f.write(pickle.dumps(var))

def load(var):
    try:
        with open(namestr(var,globals())[0], "rb") as f:
            return pickle.load(f)
    except:
        return dict()


default_param = {"chan_name": "Espace de {}",
                 "archive": "archive"
                 }


def getChanFromId(guild, _id):
    return discord.utils.get(guild.channels, id=int(_id))


def getUserFromId(guild, _id):
    return discord.utils.get(guild.members, id=int(_id))

def isEnglish(member):
    eng = "English-speaking"
    roles = [role.name for role in member.roles]
    if eng in roles:
        return True
    return False

def chooseChanName(g,chan_id):
    try:
        if guild_tab[g.id]["fork"][chan_id]["phrases"] != []:
            return random.choice(guild_tab[g.id]["fork"][chan_id]["phrases"])
    except:
        pass
    try:
        return guild_tab[g.id]["default_param"]["chan_name"]
    except:
        return default_param["chan_name"]

def getArchiveDir(g):
    return discord.utils.get(g, name=guild_tab[g.id]["default_param"]["archive"])  # can be None


def get_values(obj,tab,attr):
    return list(map(lambda tmp: getattr(tmp, attr), getattr(obj, tab)))

def contain_any(l1, l2):
    if len([elt for elt in l1 if elt in l2]) != 0:
        return True
    return  False
def allocate_new_guild(guild_id):
    guild_tab[guild_id] = {"fork": dict(), "created": dict(), "default_param": default_param}


def is_valid_chan_name(s,nb):
    cnt = 0
    prev = False
    for c in s:
        if prev is False and c == "{":
            prev = True
            continue
        if prev is True and c == "}":
            cnt +=1
        else:
            prev = False
    return cnt == nb


#######################################

# ############ #
# BOT COMMAND  #
################

## ADD DISPATCHER CHANNEL ##
@bot.command(name='add-fork-chan',
             help="Crée un nouveaux canal d'écoute\n argument : \n <identifiant du canal a ecouter>  <identifiant du canal ou le lien de la visio sera posté>" )
async def add_dispatcher_channel(ctx, channel_id: int, channel_txt_id=0):
    print("add fork chan")
    guild = ctx.guild
    if guild.id not in guild_tab.keys():
        allocate_new_guild(guild.id)
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist")
        await ctx.send("erreur ajout canal (cannal inexistant)")
    elif channel_id in guild_tab[guild.id]["fork"]:
        print("erreur ajout canal (canal vocal  deja ajouté")
        await ctx.send("erreur ajout canal (cannal vocal deja ajouté)")
    else:
        existing_channel_txt = discord.utils.get(guild.channels, id=int(channel_txt_id))
        if existing_channel_txt is None and channel_txt_id != 0:
            await ctx.send("erreur ajout canal (canal texte inexistant")
            return
        print(f"on enregistre le chan dispatcher : {channel_id} ({getChanFromId(guild,channel_id)})et le txt {channel_txt_id} ({getChanFromId(guild,channel_txt_id)})")
        # guild_tab[guild.id]["fork"][channel_id] = dict()  # not useful
        guild_tab[guild.id]["fork"][channel_id] = {"txt_chan_id": channel_txt_id,
                                                   "child_chan_txt": False,
                                                   "nb_phrase_pattern": 0,
                                                   "role": [],
                                                   "msg_txt": "Voici le lien pour la visio de {} {}",
                                                   "del_on_leave": False
                                                   }
        save(guild_tab)
        await ctx.send("canal ajouté")
@bot.command(name='del-fork-chan',
             help="Supprime un canal d'écoute\n argument : \n <identifiant du canal a supprimer>  ")
async def del_dispatcher_channel(ctx, channel_id : int):
    print("del fork chan")
    guild = ctx.guild
    if guild.id not in guild_tab.keys():
        await ctx.send("Aucune information sur le serveur de trouvé, commande ignoré")
        return

    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if existing_channel is None or channel_id not in guild_tab[guild.id]["fork"].keys():
        print("channel doesn't exist or not register")
        await ctx.send("Erreur suppression canal (n'existe pas ou n'est pas enregisté)")
    else:
        print(f"on supprime le chan dispatcher : {channel_id} ({getChanFromId(guild,channel_id)})")
        del guild_tab[guild.id]["fork"][channel_id]
        save(guild_tab)
        await ctx.send("canal supprimé")

@bot.command(name='add-named-chan',
             help="Ajoute un nom de canal possible pour les cannaux crée par les cannaux de **add-fork-chan**")
async def add_named_chan(ctx, channel_id : int, *remain):
    print(f"add sentence for {channel_id}")
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist or not register")
        await ctx.send(f"le canal {existing_channel.name if existing_channel is not None else existing_channel} n'est pas enrigistré dans les canaux d'écoute")
        return

    if guild.id not in guild_tab.keys():
        allocate_new_guild(guild.id)

    if channel_id not in guild_tab[guild.id]["fork"].keys():
        await add_dispatcher_channel(ctx, channel_id)



    guild_tab[guild.id]["fork"][channel_id]["nb_phrase_pattern"] += len([r for r in remain if is_valid_chan_name(r, 1)])
    if "phrases" not in guild_tab[guild.id]["fork"][channel_id].keys():
        guild_tab[guild.id]["fork"][channel_id]["phrases"] = list()
    guild_tab[guild.id]["fork"][channel_id]["phrases"].extend([r for r in remain if is_valid_chan_name(r, 1)])
    save(guild_tab)
    await ctx.send(f"Noms ajoutés sauf : {[r for r in remain if not is_valid_chan_name(r, 1)]}")

@bot.command(name='del-named-chan',
             help="Supprime un nom de canal possible pour les cannaux crée par les cannaux de **add-fork-chan**")
async def del_named_chan(ctx, channel_id : int, *to_del):
    print(f"del sentence for {channel_id}")
    guild = ctx.guild
    if guild.id not in guild_tab.keys():
        await ctx.send("Aucune information trouvé")
        return

    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if existing_channel is None or channel_id not in guild_tab[guild.id]["fork"].keys():
        print("channel doesn't exist")
        await ctx.send("erreur suppression texte")
    else:
        for elt in [r for r in to_del]:
            print(elt, guild_tab[guild.id]["fork"][channel_id]["phrases"])
            if elt in guild_tab[guild.id]["fork"][channel_id]["phrases"]:
                guild_tab[guild.id]["fork"][channel_id]["nb_phrase_pattern"] -= 1
                guild_tab[guild.id]["fork"][channel_id]["phrases"].remove(elt)


        save(guild_tab)
        await ctx.send("textes supprimé")

@bot.command(name='add-role-for-chan',
             help="Seul les personnes possedant ces role pourront ouvrir des canaux  **add-fork-chan**")
async def add_role_chan(ctx, channel_id: int, *to_add):
    print(f"add role for {channel_id}")
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist")
        await ctx.send("erreur ajout roles (canal n'existe pas)")
        return

    if guild.id not in guild_tab.keys():
        allocate_new_guild(guild.id)

    if channel_id not in guild_tab[guild.id]["fork"].keys():
        await add_dispatcher_channel(ctx, channel_id)


    guild_roles = get_values(guild, "roles", "name")
    print(to_add, guild_roles, guild_tab[guild.id]["fork"][channel_id]["role"])
    guild_tab[guild.id]["fork"][channel_id]["role"].extend([r for r in to_add if r in guild_roles and r not in guild_tab[guild.id]["fork"][channel_id]["role"]])
    print(f"les roles autorisé : {guild_tab[guild.id]['fork'][channel_id]['role']}")
    save(guild_tab)
    await ctx.send(f"roles autorisé : {guild_tab[guild.id]['fork'][channel_id]['role']}")


@bot.command(name='del-role-for-chan',
             help="Supprime les roles des accès a ce chan")
async def del_role_chan(ctx, channel_id: int, *remain):
    print(f"del role for {channel_id}")
    guild = ctx.guild
    if guild.id not in guild_tab.keys():
        await ctx.send("Aucune information trouvé")
        return
    existing_channel = getChanFromId(guild, channel_id)
    if not existing_channel and channel_id not in guild_tab[guild.id]["fork"].keys():
        print("channel doesn't exist or not register")
        await ctx.send("erreur suppression roles (le canal n'existe pas ou n'est pas enregistré")
    else:
        for role in remain:
            try:
                guild_tab[guild.id]["fork"][channel_id]["role"].remove(role)
            except:
                print("elt not in list")
        save(guild_tab)
        await ctx.send("roles supprimé")


@bot.command(name='set-chan-txt-creation-for-child',
             help="Modifie le gestion des chan txt créent par les chan fils")
async def set_txt_creation_for_child(ctx, channel_id: int, txt: bool, archive: bool):
    print(f"modify  {channel_id} child txt creation")
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist")
        await ctx.send("erreur dans l'ajout de chan txt des chan crée")
        return

    if guild.id not in guild_tab.keys():
        allocate_new_guild(guild.id)

    if channel_id not in guild_tab[guild.id]["fork"].keys():
        await add_dispatcher_channel(ctx, channel_id)

    guild_tab[guild.id]["fork"][channel_id]["child_chan_txt"] = txt
    guild_tab[guild.id]["fork"][channel_id]["child_txt_archive"] = archive
    save(guild_tab)
    await ctx.send(f"les chan créent par {getChanFromId(guild,channel_id)}   { 'auront' if txt else 'n auront pas' } de chan txt de crée et ils {'seront' if archive else 'ne seront pas'} archivés" )


@bot.command(name='set-msg-for-created-chan',
             help="Modifie le gestion des chan txt créent par les chan fils")
async def set_msg_for_child(ctx, channel_id: int, txt):
    print(f"modify  {channel_id}  txt for visio")
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist")
        await ctx.send("erreur dans la modification du message ")
        return

    if guild.id not in guild_tab.keys():
        allocate_new_guild(guild.id)

    if channel_id not in guild_tab[guild.id]["fork"].keys():
        await add_dispatcher_channel(ctx, channel_id)

    if guild_tab[guild.id]["fork"][channel_id]["txt_chan_id"] == 0:
        await ctx.send(f"erreur : le canal {getChanFromId(guild,channel_id)} doit etre lié avec un canal texte")
        await ctx.send(f"utilisez la fonction : bind-with-chan-txt <id canal d'écoute> <id canal texte>")
        return
    if not is_valid_chan_name(txt, 2):
        ctx.send("le message doit contenir 2 {}")
        return
    guild_tab[guild.id]["fork"][channel_id]["msg_txt"] = txt
    save(guild_tab)
    await ctx.send("mise a jour du texte personnalisé envoyé a la création d'un chan")


@bot.command(name="unbind-chan-txt",
             help="Supprime la liaison d'un chan d'écoute avec le chan texte")
async def unbind(ctx, channel_id: int):
    await bind_with_chan_txt(ctx, channel_id, 0)


@bot.command(name='bind-with-chan-txt',
             help="modifie le gestion des chan txt créent par les chan fils")
async def bind_with_chan_txt(ctx, channel_id: int, chan_txt_id: int):
    print(f"modify  {channel_id} link chan txt")
    guild = ctx.guild

    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel:
        print("channel doesn't exist")
        await ctx.send("erreur : canal vocal inexistant")

    if guild.id not in guild_tab.keys():
        allocate_new_guild(guild.id)


    if channel_id not in guild_tab[guild.id]["fork"].keys():
        await add_dispatcher_channel(ctx, channel_id, chan_txt_id)
        return

    existing_channel_txt = discord.utils.get(guild.channels, id=int(chan_txt_id))
    if existing_channel_txt is None and chan_txt_id != 0:
        print("channel doesn't exist")
        await ctx.send("erreur : canal texte inexistant")

    guild_tab[guild.id]["fork"][channel_id]["txt_chan_id"] = chan_txt_id
    save(guild_tab)
    await ctx.send("mise a jour du chan txt utilisé par les salon créent")


@bot.command(name='del-on-leave',
             help="modifie le gestion des chan txt créent par les chan fils")
async def del_on_leave(ctx, channel_id: int, to_del: bool, delay=0):
    print(f"modify  {channel_id}  (del on leave)")
    guild = ctx.guild
    if guild.id not in guild_tab.keys():
        print("make chan before use this function")
    existing_channel = discord.utils.get(guild.channels, id=int(channel_id))
    if not existing_channel and channel_id not in guild_tab[guild.id]["fork"].keys():
        print("channel doesn't exist")
        await ctx.send("le chan n'est pas enregistré dans le bot")
    else:
        guild_tab[guild.id]["fork"][channel_id]["del_on_leave"] = to_del
        guild_tab[guild.id]["fork"][channel_id]["delay"] = delay
        save(guild_tab)
        await ctx.send("mise a jour ok")


# ####### ############# ####### #
# ####### DEFAULT PARAM ####### #
# ####### ############# ####### #
@bot.command(name='change-default-chan-name',
             help="modifie le nom par défaut des chans crée")
async def set_default_name_to_child(ctx, name="Espace de {}"):
    guild = ctx.guild
    if guild.id not in guild_tab.keys():
        allocate_new_guild(guild)
    if is_valid_chan_name(name, 1):
        guild_tab[guild.id]["default_param"]["chan_name"] = name
        await ctx.send("nom par défaut changé")
    else:
        await ctx.send("il faut que le nom par defaut contiene au moins un '{}' pour etre valide")


@bot.command(name='set-archive-category',
             help="Modifie la catégorie servant a archivé les salons textuels")
async def set_default_archive(ctx, arch_id : int):
    guild = ctx.guild
    if guild.id not in guild_tab.keys():
        allocate_new_guild(guild.id)
    cat = discord.utils.get(guild.categories, id=arch_id)
    if cat is None:
        await ctx.send("cette categorie n'existe pas")
        return
    guild_tab[guild.id]["default_param"]["archive_id"] = arch_id
    await ctx.send("dossier d'archivage par defaut changé")
# ############################ #
# ############################ #
# ############################ #


@bot.command(name="clean-created")
async def clean_created(ctx):
    if ctx.guild.id in guild_tab.keys():
        guild_tab[ctx.guild.id]["created"] = dict()
    save(guild_tab)


@bot.command(name="clean-all")
async def clean_all(ctx):
    if ctx.guild.id in guild_tab.keys():
        guild_tab[ctx.guild.id]["fork"] = dict()
        guild_tab[ctx.guild.id]["created"] = dict()
        guild_tab[ctx.guild.id]["default_param"] = dict()
    save(guild_tab)
##############################################
#                EVENT BOT                   #
##############################################


def is_chan_in_forkeur(guild, chan):
    try:
        if chan is None:
            return False
        if chan.id in guild_tab[guild.id]["fork"]:
            return True
        else:
            return False
    except:
        return False


def is_chan_in_created(guild, chan):
    try:
        if chan is None:
            return False
        if chan.id in guild_tab[guild.id]["created"]:
            return True
        else:
            return False
    except:
        return False


# # ADD REATION ON PEOPLE  WHEN ENTERING IN SERVER # #
@bot.event
async def on_message(message):
    try:
        if contain_any(get_values(message.author,"roles","name"), ["Doom Guy", "Orga"]) and message.content[0] == "£":
            await bot.process_commands(message)
        elif message.content[0] == "£":
            await message.channel.send("Sorry you don't have the permission to do this")
    except:
        print("no msg")


@bot.event
async def on_member_join(member):
    pass


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
        channel_info = guild_tab[guild.id]["fork"][after.channel.id]
        member_role = get_values(member, "roles", "name")  # list(map(lambda role: role.name, member.roles))
        name = member.display_name
        channel_name_pattern = chooseChanName(guild, after.channel.id)
        print(channel_name_pattern)
        channel_name = channel_name_pattern.format(name)
        if guild.id == 693172975045705819:
            if "English-speaking" in member_role:
                channel_name = "*en* " + channel_name

        print("creation du canal :" + channel_name + " text will be " + guild_tab[guild.id]["fork"][after.channel.id]["msg_txt"])
        print(f"user role {member_role} , {channel_info['role']}, {len(channel_info['role']) }")
        if len(channel_info["role"]) == 0 or contain_any(member_role, channel_info["role"]):
            print("check roles : ok")
            cat = discord.utils.get(guild.categories, id=after.channel.category_id)
            created_chan = await guild.create_voice_channel(channel_name, category=cat)
            guild_tab[guild.id]["created"][created_chan.id] = dict()
            guild_tab[guild.id]["created"][created_chan.id]["parent"] = after.channel.id
            guild_tab[guild.id]["created"][created_chan.id]["creator"] = member.id
            guild_tab[guild.id]["created"][created_chan.id]["title"] = channel_name_pattern

            if channel_info["txt_chan_id"] != 0:
                msg = await getChanFromId(guild, channel_info["txt_chan_id"]).send(channel_info["msg_txt"].format(member.mention, "🎬 https://discordapp.com/channels/" + str(guild.id)+"/"+str(created_chan.id)))

                guild_tab[guild.id]["created"][created_chan.id]["msg_id"] = msg.id

                if channel_info["child_chan_txt"] is True:
                    created_txt_chan = await guild.create_text_channel("txt-"+channel_name, category=cat)
                    guild_tab[guild.id]["created"][created_chan.id]["perso_txt_chan_id"] = created_txt_chan.id
            await member.move_to(created_chan)
        else:
            print("role not ok : leave")
            await member.move_to(None)



    if is_chan_in_created(guild, before.channel) :
        print("before in created chan")
        parent_id = guild_tab[guild.id]["created"][before.channel.id]["parent"]
        # print(parent_id, guild_tab[guild.id]["fork"].values())
        if parent_id not in guild_tab[guild.id]["fork"].keys():
            print("bug, value changed ...")
            return

        parent_info = guild_tab[guild.id]["fork"][parent_id]
        current_info = guild_tab[guild.id]["created"][before.channel.id]
        #print(parent_info)
        #print(current_info)
        to_del = False
        if "del_on_leave" in parent_info.keys():
            to_del = parent_info["del_on_leave"]
        print("ok 1")
        if len(before.channel.members) == 0 or (to_del is True and member.id == current_info["creator"]):

            print(f"del voice chan ")
            if "delay" in parent_info.keys():
                print(f"wait {parent_info['delay']} seconds")
                await asyncio.sleep(parent_info['delay'])
                if member in before.channel.members:
                    print("still in")
                    return
                benevole = None
                for person in before.channel.members:
                    if "benevole workshop" in get_values(person,"roles","name"):
                        benevole = person
                        break
                if benevole is not None:
                    print("benevole in")
                    return


            try:
                await before.channel.delete()
            except:
                print("skip delete chan voice")
            if parent_info["txt_chan_id"] != 0:  # it have to delete msg
                try:
                    await (await getChanFromId(guild, parent_info["txt_chan_id"]).fetch_message(current_info["msg_id"])).delete()
                except:
                    print("skip delte msg")
            if "perso_txt_chan_id" in current_info.keys():  # it have to delete chan txt perso
                print("child have chan txt")
                if parent_info["child_txt_archive"] is True: # NO archive it
                    print("make archive later")
                    chan = getChanFromId(guild, current_info["perso_txt_chan_id"])
                    await chan.edit(
                        name=chan.name,
                        topic=chan.topic,
                        position=0,
                        sync_permissions=True,
                        category=discord.utils.get(guild.channels, name="archive")
                    )
                    pass  # move chan txt to saved zone
                else: # delete chan txt of child
                    print("del chan txt")
                    try:
                        await getChanFromId(guild, current_info["perso_txt_chan_id"]).delete()  # change this later
                    except:
                        print("skip delete chan")
            del guild_tab[guild.id]["created"][before.channel.id]

        elif to_del is False and member.id == current_info["creator"]:
            print("leave chan and i'm the creator")
            new_creator = before.channel.members[0].id
            print(f"new creator is {getUserFromId(guild, new_creator).display_name }")
            if parent_info["txt_chan_id"] != 0:
                msg = getChanFromId(guild,parent_info["txt_chan_id"]).fetch_message(current_info["msg_id"])
                await msg.edit(content=parent_info["msg_txt"].format(new_creator.mention,
                                                                     "🎬 https://discordapp.com/channels/" + str(
                                                                         guild.id) + "/" + str(before.channel.id)))
            current_info["creator"] = new_creator  # getUserFromId(guild, new_creator).display_name
            chan_name = guild_tab[guild.id]["created"][before.channel.id]["title"].format(getUserFromId(guild, current_info["creator"]).display_name)
            print(f"new chan name : {chan_name}")
            await before.channel.edit(name=chan_name)

    save(guild_tab)


@bot.event
async def on_ready():
    print("bot online")
@bot.command()
async def join(ctx):
    chan = ctx.message.author.voice.channel
    print(chan.name)
    if chan is None:
       await ctx.send("vous devez etre en vocal ;)")
    else:
        await chan.connect()

@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    await voice_client.disconnect()

@bot.command()
async def play(ctx):
    vc = await ctx.message.author.voice.channel.connect()
    player = discord.FFmpegPCMAudio('song.mp3', executable=".\\ff_mpeg_windows\\bin\\ffmpeg.exe")
    vc.play(player)


guild_tab = load(guild_tab)

bot.run(TOKEN)

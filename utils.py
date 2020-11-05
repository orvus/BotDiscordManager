import discord
import pickle


def get_values(obj,tab,attr):
    return list(map(lambda tmp: getattr(tmp, attr), getattr(obj, tab)))

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

#TODO save var with part of fileName for evoid name collision
def save(var,name):
    with open(name, "wb+") as f:
        f.write(pickle.dumps(var))

def load(name):
    try:
        with open(name, "rb") as f:
            return pickle.load(f)
    except:
        return dict()

def getChanFromId(guild, _id):
    return discord.utils.get(guild.channels, id=int(_id))

def getUserFromId(guild, _id):
    return discord.utils.get(guild.members, id=int(_id))

def contain_any(l1, l2):
    if len([elt for elt in l1 if elt in l2]) != 0:
        return True
    return False

import discord
from pathlib import Path
import sys, os

def combine_paths(path1 : str, path2: str):
    path2_real = ""
    if "/" in path1:
        path2_real = path2.replace("\\", "/")
        return path1 + "/" + path2
    else:
        path2_real = path2.replace("/", "\\")
        return path1 + "\\" + path2_real

def get_guild_folder(guild : discord.Guild):
    path = Path(__file__)

    newpath = ""
    if "/" in str(path.parent):
        newpath = str(path.parent.absolute()) + "/" + "db" + "/" + guild.name
    else:
        newpath = str(path.parent.absolute()) + "\\" + "db" + "\\" + guild.name
    return newpath

def create_directory_in_parent(name : str):
    path = Path(__file__)

    newpath = ""
    if "/" in str(path.parent):
        newpath = str(path.parent.absolute()) + "/" + name
    else:
        newpath = str(path.parent.absolute()) + "\\" + name
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def create_guild_directory(name : str):
    path = Path(__file__)

    newpath = ""
    if "/" in str(path.parent):
        newpath = str(path.parent.absolute()) + "/" + "db" + "/" + name
    else:
        newpath = str(path.parent.absolute()) + "\\" + "db" + "\\" + name
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def create_user_directory(message : discord.Message = None, member : discord.Member = None):
    newpath = get_user_directory(message=message, member=member)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    if not os.path.exists(combine_paths(newpath, "level.txt")):
        with open(combine_paths(newpath, "level.txt"), 'w') as file:
            # Write content to the file
            file.write(str(0))

def get_user_directory(message : discord.Message = None, member : discord.Member = None):
    member_name = ""
    guild_dir = ""
    if message == None:
        member_name = member.name
        guild_dir = get_guild_folder(member.guild)
    else:
        member_name = message.author.name
        guild_dir = get_guild_folder(message.guild)
    
    newpath = ""
    if "/" in str(guild_dir):
        newpath = guild_dir + "/" + member_name
    else:
        newpath = guild_dir + "\\" + member_name
    return newpath
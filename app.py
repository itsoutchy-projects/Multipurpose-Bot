import math
import discord
from discord import app_commands
import sys, os
from pathlib import Path
import config
import shutil
import embeds
import asyncio
from enums import *
import paths

# Code written by itsoutchy
# Please do not remove this comment
# Thanks!

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

bot_prefix = "mb!"

single_level_XP = 100

XP_per_message = 10
booster_XP_per_message = 20

activity = discord.Activity(type=discord.ActivityType.watching, name="mb!hello")

support_server_link = "https://discord.gg/QF8pN88VEM"
website_link = "https://multipurposebot.itsoutchy.xyz/"

bug_report_webhook_URL = "https://discord.com/api/webhooks/1284278357957148713/MXca1cxd72t6J5CnORwrpV4ifcoUIFlXtRz-Ep-EFUAkoHz320UelOCe-dci_fudLeLW"

bug_report_channel_ID = 1284278273051857032

spam_interval = 5
spam_count = 5

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")
    await client.change_presence(activity=activity)
    for guild in client.guilds:
        paths.create_directory_in_parent(guild.name)

@client.event
async def on_guild_join(guild : discord.Guild):
    print("Joined server, start storing info")
    paths.create_directory_in_parent(guild.name)

#region levelling system

def add_XP(user : discord.Member):
    if user.bot:
        return
    newpath = paths.get_user_directory(member=user)
    if not os.path.exists(newpath):
        paths.create_user_directory(member=user)
    print(paths.combine_paths(newpath, "level.txt"))
    with open(paths.combine_paths(newpath, "level.txt"), 'r+') as file:
        # Write content to the file
        if not file.readable():
            # file is not readable for some reason, the tip doesn't show the exact reason but it's one I found while coding this
            print("ERROR: add_XP(discord.Member) file object is not readable")
            print("TIP: Check the mode, to have it be both readable and writable, change it to \"r+\"")
            return
        xp = file.read() # read the file
        file.seek(0) # go to the beginning because for some [censored] reason it doesn't DO THAT AUTOMATICALLY, THERES A [censored] APPEND FUNCTION FOR A REASON
        print(xp) # debugging
        if not user in user.guild.premium_subscribers:
            new_xp = int(xp) + XP_per_message # add regular XP
        else:
            new_xp = int(xp) + booster_XP_per_message # add boosted XP, thanks for boosting the server!
        print(new_xp) # debugging
        file.write(f"{new_xp}") # write the new amount to the data file

def set_XP(user : discord.Member, new_XP : int):
    newpath = paths.get_user_directory(member=user)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    print(paths.combine_paths(newpath, "level.txt"))
    if not os.path.exists(paths.combine_paths(newpath, "level.txt")):
        with open(paths.combine_paths(newpath, "level.txt"), "x+") as file:
            file.write("0")
    with open(paths.combine_paths(newpath, "level.txt"), 'r+') as file:
        # Write content to the file
        if not file.readable():
            # file is not readable for some reason, the tip doesn't show the exact reason but it's one I found while coding this
            print("ERROR: add_XP(discord.Member) file object is not readable")
            print("TIP: Check the mode, to have it be both readable and writable, change it to \"r+\"")
            return
        #file.read() # nvm im dumb
        file.seek(0) # go to the beginning because for some [censored] reason it doesn't DO THAT AUTOMATICALLY, THERES A [censored] APPEND FUNCTION FOR A REASON
        file.write(f"{new_XP}") # write the new amount to the data file
        file.truncate()
        # not again whats wrong this time :/

def read_level(user : discord.Member):
    newpath = paths.get_user_directory(member=user)
    if not os.path.exists(newpath):
        return 1 # code for no rank
    if not os.path.exists(paths.combine_paths(newpath, "level.txt")):
        return 1 # code for no rank
    
    if os.path.exists(paths.combine_paths(newpath, "level.txt")):
        with open(paths.combine_paths(newpath, "level.txt"), "r+") as file:
            # Write content to the file
            return str(math.floor(int(file.read()) / single_level_XP))
        
def read_XP(user : discord.Member):

    newpath = paths.get_user_directory(member=user)
    if not os.path.exists(newpath):
        return 1 # code for no rank
    if not os.path.exists(paths.combine_paths(newpath, "level.txt")):
        return 1 # code for no rank
    
    if os.path.exists(paths.combine_paths(newpath, "level.txt")):
        with open(paths.combine_paths(newpath, "level.txt"), "r+") as file:
            # Write content to the file
            return str(file.read())
        
#endregion



@client.event
async def on_message(msg : discord.Message):
    try:
        if msg.author == client.user or msg.webhook_id != None or msg.author.bot:
            return
        
        #if  msg.created_at.timestamp()
        
        path = Path(__file__)

        newpath = paths.get_user_directory(message=msg)
        if not os.path.exists(newpath):
            paths.create_user_directory(msg) # why cant message.author always return a member and not a user
        else:
            if "/" in str(path.parent):
                if not os.path.exists(newpath + "/level.txt"):
                    with open(newpath + "/level.txt", "x") as f:
                        f.write("0")
            else:
                if not os.path.exists(newpath + "\\level.txt"):
                    with open(newpath + "\\level.txt", "x") as f:
                        f.write("0")
            add_XP(msg.author)
            # Level roles
            path = Path(__file__)
            newpath = paths.get_guild_folder(msg.guild) + "/level_roles.txt"
            with open(newpath, "r") as file:
                entries = file.read().splitlines()
                for line in entries:
                    if not line == "" and not line == "\n":
                        entry = line.split("=")
                        if int(read_level(msg.author)) >= int(entry[0]):
                            if not msg.author.guild.get_role(int(entry[1])) in msg.author.roles:
                                await msg.author.add_roles(msg.author.guild.get_role(int(entry[1])))
        
        # Text commands
        if msg.content.startswith(f"{bot_prefix}hello"):
            embed = helloEmbed()
            await msg.reply(embed=embed)
        if msg.content.startswith(f"{bot_prefix}sync"):
            if msg.author.id == 557219247227404315:
                await msg.reply("Syncing slash commands, this may take a while...")
                await tree.sync()
            else:
                await msg.reply(embeds.bot_dev_only)
        if msg.content.startswith(f"{bot_prefix}purge"):
            cmd = msg.content.split(" ")
            num = 0
            if msg.author.guild_permissions.manage_messages:
                if int(cmd[1]) == 0:
                    num = len(await msg.channel.purge())
                else:
                    num = len(await msg.channel.purge(limit=int(cmd[1])))
                await msg.channel.send(embed=discord.Embed(colour=discord.Colour.green(), title="Success!", description=f"Successfully deleted {num} messages"))
            else:
                await msg.reply(embed=embeds.insufficient_permissions(Permissions.MANAGE_MESSAGES))
    except Exception as e:
        await msg.channel.send(embed=embeds.error(e))

@client.event
async def on_guild_remove(guild : discord.Guild):
    if guild.name != None:
        shutil.rmtree(paths.get_guild_folder(guild))

@tree.command(name="hello", description="Useful info about Multipurpose Bot")
async def hello(interaction : discord.Interaction):
    await interaction.response.send_message(embed=helloEmbed())

@tree.command(name="report_bugs", description="Report a bug with the bot")
async def report_bugs(interaction : discord.Interaction, message : str):
    # webhook = discord.Webhook.from_url(url=bug_report_webhook_URL, client=client) # should send from the client so we can edit it later
    embed = discord.Embed(colour=embeds.main_colour, title="Bug Report", description=message)
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text="React with ✅ when solved")
    channel = client.get_channel(bug_report_channel_ID)
    await channel.send(content="<@&1284455138924302377>", embed=embed)
    msg = f"<:tick:1270546288534093865> Success!\n\nYour report's url is: {channel.last_message.jump_url}"
    if not client.get_guild(1270703846003310663) in interaction.user.mutual_guilds:
        msg += f"\nShowing unknown for you? Join the support server to track your report: {support_server_link}"
    await interaction.response.send_message(msg)

@client.event
async def on_raw_reaction_add(payload : discord.RawReactionActionEvent):
    if not payload.channel_id == bug_report_channel_ID or not payload.emoji == discord.PartialEmoji(name="\U00002705"):
        return
    print(f"Bug report: {payload.message_id} by {payload.member.display_name} is solved!")
    channel = client.get_channel(payload.channel_id)
    message = await channel.get_partial_message(payload.message_id).fetch()
    embed = message.embeds[0]
    embed.color = discord.Colour(0x2ECC71)
    embed.title = f"(SOLVED) {embed.title}"
    await message.edit(embed=embed)

@tree.command(name="purge", description="Purges messages in the current channel")
async def purge(interaction : discord.Interaction, limit : int):
    try:
        await interaction.response.defer()
        global purge_interaction
        purge_interaction = interaction
        if interaction.user.guild_permissions.manage_messages:
            deleted = 0
            if limit == 0:
                deleted = len(await interaction.channel.purge(check=is_me))
            else:
                deleted = len(await interaction.channel.purge(limit=limit, check=is_me))
            await interaction.followup.send(f"<:tick:1270546288534093865> Successfully deleted {deleted} messages")
        else:
            embed = embeds.insufficient_permissions(Permissions.MANAGE_MESSAGES)
            await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.channel.send(embed=embeds.error(e))
        try:
            await interaction.delete_original_response()
        except:
            pass # do nothing

def is_me(message : discord.Message):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(is_me_inner(message))

async def is_me_inner(message : discord.Message):
    return not message == await purge_interaction.original_response()

@tree.command(name="add_level_role", description="Adds a new level role")
async def add_level_role(interaction : discord.Interaction, level : int, role : discord.Role):
    if interaction.user.guild_permissions.manage_guild:
        newpath = paths.get_guild_folder(interaction.guild) + "/level_roles.txt"
        with open(newpath, "a") as file:
            file.write(f"{level}={role.id}\n")
        await interaction.response.send_message("<:tick:1270546288534093865> Success!")
    else:
        await interaction.response.send_message(embed=embeds.insufficient_permissions(Permissions.MANAGE_SERVER))

@tree.command(name="remove_level_role", description="Remove a level role")
async def remove_level_role(interaction : discord.Interaction, level : int):
    try:
        if interaction.user.guild_permissions.manage_guild:
            newpath = paths.get_guild_folder(interaction.guild) + "/level_roles.txt"
            role_to_replace = ""
            with open(newpath, "r+") as file:
                oldfile = file.read()
                
                file.seek(0)
                file.truncate(0)
                for line in oldfile.splitlines(keepends=True):
                    if not line.startswith(str(level)):
                        file.write(line) # you should actually write it
            await interaction.response.send_message("<:tick:1270546288534093865> Success!")
        else:
            await interaction.response.send_message(embed=embeds.insufficient_permissions(Permissions.MANAGE_SERVER))
    except Exception as e:
        embed = embeds.error(e)
        await interaction.response.send_message(embed=embed)

def helloEmbed():
    embed = discord.Embed(colour=embeds.main_colour, title="Hi!", description=f"Thank you for adding Multipurpose Bot to your server.\n\nHere is a list of my commands!\n</rank:1270162430437359626> - check your level\n</role_all:1270131706678214700> - adds a role to all members\n</unrole_all:1270137326529679400> - removes a role from all members\n</set_xp:1270512705677299723> - set a member's level\n</add_level_role:1280509314280456217> - add a role you can earn by levelling up\n</topic_change:1280117702463328306> - request a topic change\n</report_bugs:1284282522007633945> - report a bug\nMore to be added soon!\n\n**Credits**\nBot developed by [itsoutchy](<https://itsoutchy.xyz>)\n\nSupport server: {support_server_link}\nWebsite: {website_link}")
    embed.set_footer(text="Made with ❤️ in discord.py")
    embed.set_thumbnail(url=client.user.avatar.url)
    return embed

def firstItemInTuple(tuple : tuple):
    return tuple[0]

def leaderboardEmbed(guild : discord.Guild, all_users : bool = False):
    members = list[discord.Member]
    #test = ("10", members[0])
    lvls = list[tuple]()
    for mem in guild.members:
        if not mem.bot:
            lvl = read_level(mem)
            if not lvl == 1 and not lvl == None:
                lvls.append((int(lvl), mem))
                #lvls.insert(lvls, len(lvls), (lvl, mem))
    lvls.sort(key=lambda tup: tup[0], reverse=True)
    description = ""
    i = 1
    for t in lvls:
        description += f"{i}. {t[1]}: {t[0]}\n"
        if i == 10 and not all_users:
            break
        i += 1
    embed = discord.Embed(colour=embeds.main_colour, title=f"{guild.name}'s Leaderboard", description=description)
    if not all_users:
        embed.set_footer(text="Displays the top 10")
    return embed

def get_rank(mem : discord.Member):
    members = list[discord.Member]
    #test = ("10", members[0])
    guild = mem.guild
    lvls = list[tuple]()
    for mem in guild.members:
        if not mem.bot:
            lvl = read_level(mem)
            if not lvl == 1 and not lvl == None:
                lvls.append((int(lvl), mem))
                #lvls.insert(lvls, len(lvls), (lvl, mem))
    lvls.sort(key=lambda tup: tup[0], reverse=True)
    description = ""
    i = 1
    for t in lvls:
        if f"{t[1]}" == f"{mem}":
            break
        i += 1
    return i

@tree.command(name="lb", description="See the leaderboard for this server")
async def lb(interaction : discord.Interaction, all_users : bool = False):
    emb = leaderboardEmbed(interaction.guild, all_users)
    emb.set_thumbnail(url=interaction.guild.icon.url)
    await interaction.response.defer()
    await interaction.followup.send(embed=emb)

@tree.command(name="clear", description="Clears all of your info, either server specific or globally")
async def clear(interaction : discord.Interaction, globally : bool):
    await interaction.response.defer()
    if globally:
        for guild in client.guilds:
            if interaction.user in guild.members:
                newpath = paths.get_user_directory(member = interaction.user)
                if os.path.exists(newpath):
                    shutil.rmtree(newpath)
                    print(f"Removed {interaction.user.name}'s directory for {guild.name}")
    else:
        guild = interaction.guild
        if interaction.user in guild.members:
                newpath = paths.get_user_directory(member = interaction.user)
                if os.path.exists(newpath):
                    shutil.rmtree(newpath)
                    print(f"Removed {interaction.user.name}'s directory for {guild.name}")
    await interaction.followup.send("<:tick:1270546288534093865> Successfully cleared your information")

@tree.command(name="topic_change", description="Request a topic change")
async def topic_change(interaction : discord.Interaction, message : str = ""):
    embed = discord.Embed(colour=embeds.main_colour, title="Topic change", description="A topic change has been requested, please change topics to avoid moderation")
    if not message == "":
        embed = discord.Embed(colour=embeds.main_colour, title="Topic change", description=message)
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="rank", description="Check your level")
async def rank(interaction : discord.Interaction, member : discord.Member | None):
    # PLEASE TELL ME THIS WILL WORK PLEEEAAAAASEEEEEE
    await interaction.response.defer()
    user = interaction.user
    if not member == None:
        user = member
    if user.bot:
        await interaction.followup.send("<:X_:1270546327788585041> This user is a bot, bots don't have a level")
        return
    level = read_level(user)
    if level == 1:
        await interaction.followup.send("<:X_:1270546327788585041> You have no level, chat to get one")
        return
    xp = read_XP(user)
    embed = discord.Embed(colour=embeds.main_colour, title=f"{user.display_name}'s level", description=f"level: {level}\nXP: {xp}\n-# Each level requires 100 XP, chat to gain XP")
    embed.set_thumbnail(url=user.display_avatar.url)
    await interaction.followup.send(embed=embed)

@tree.command(name="set_xp", description="Set a member's XP (requires manage server permission)")
async def set_level(interaction : discord.Interaction, member : discord.Member, new_xp : int):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(embed=embeds.insufficient_permissions(Permissions.MANAGE_SERVER))
        return
    set_XP(member, new_xp)
    await interaction.response.send_message(f"<:tick:1270546288534093865> Successfully set {member.display_name}'s XP")

@tree.command(name="role_all", description="Adds a role to everyone in the server")
async def role_all(interaction : discord.Interaction, role : discord.Role):
    # Ratelimits might get this broken :(
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message(embed=embeds.insufficient_permissions(Permissions.MANAGE_ROLES))
        return
    await interaction.response.defer()
    failed_members = list[int]()
    for member in interaction.guild.members:
        try:
            await member.add_roles(role)
        except:
            failed_members.append(failed_members, member.id)
            print(failed_members)
    if len(failed_members) > 0:
        failed_mentions = ""
        for mem in failed_members:
            failed_mentions = " ".join([failed_mentions, f"<@{mem}>"])
        embed = discord.Embed(colour=embeds.main_colour, title="Failed members", description=f"Failed on: {failed_mentions}")
        embed.set_footer("Try moving my role above their highest roles")
        await interaction.followup.send("<:tick:1270546288534093865> Done!", embed=embed)
    else:
        await interaction.followup.send("<:tick:1270546288534093865> Done!")

@tree.command(name="unrole_all", description="Removes a role from everyone in the server")
async def unrole_all(interaction : discord.Interaction, role : discord.Role):
    # Ratelimits might get this broken :(
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message(embed=embeds.insufficient_permissions(Permissions.MANAGE_ROLES))
        return
    await interaction.response.defer()
    failed_members = list[int]()
    for member in interaction.guild.members:
        try:
            await member.remove_roles(role)
        except:
            failed_members.append(failed_members, member.id)
            print(failed_members)
    if len(failed_members) > 0:
        failed_mentions = ""
        for mem in failed_members:
            failed_mentions = " ".join([failed_mentions, f"<@{mem}>"])
        embed = discord.Embed(colour=embeds.main_colour, title="Failed members", description=f"Failed on: {failed_mentions}")
        embed.set_footer("Try moving my role above their highest roles")
        await interaction.followup.send("<:tick:1270546288534093865> Done!", embed=embed)
    else:
        await interaction.followup.send("<:tick:1270546288534093865> Done!")

token = config.TOKEN
client.run(token)
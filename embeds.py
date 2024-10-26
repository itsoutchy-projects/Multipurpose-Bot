import discord

"Collection of embeds. Please use this for consistency"
main_colour = discord.colour.Color.red()

bot_dev_only = discord.Embed(colour=main_colour, title="Insufficient permissions", description=f"You do not have sufficient permissions.\n\nThis command is for the bot developer only")

def insufficient_permissions(permission : str):
    "Returns an insufficient permissions embed"
    return discord.Embed(colour=main_colour, title="Insufficient permissions", description=f"You do not have sufficient permissions.\n\nRequired permission(s): `{permission.upper().replace(" ", "_")}`")

def error(error : Exception):
    return discord.Embed(colour=main_colour, title="Error", description=f"<:X_:1270546327788585041> Sorry! Multipurpose bot encountered an error!\n\n##Debug Info\nError Message: {error}")
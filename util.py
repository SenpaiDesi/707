import json
import discord
import sqlite3
from discord import app_commands
import aiosqlite
from datetime import datetime
logname = datetime.now()
logname_pretty = logname.strftime("%d-%m-%Y")
logname_file = str(logname_pretty)
curremt_time = datetime.now()
current_time_fancy = curremt_time.strftime("%d-%m-%Y-%H:%M:%S")


async def connect_database():
    return await aiosqlite.connect("./database.db")

def load_json(path):
    with open(path) as f:
        return json.load(f)
    

def is_bot_admin():
    async def predicate(interaction: discord.Interaction):
        if is_bot_developer(interaction.user.id):
            return True
    return app_commands.check(predicate)


def is_bot_developer(member_id):
    database = sqlite3.connect("./database.db")
    try:
        listdevs = database.execute(
            f"SELECT * FROM botdevs WHERE userid = {member_id}")
        returndevs = listdevs.fetchall()
        if not returndevs:
            database.close()
            return False
        else:
            database.close()
            return True
    except ValueError:
        pass


def create_embed(title, color):
    """Creates a Discord embed and returns it (for potential additional modification)"""
    embed = discord.Embed(title=title, color=color)
    return embed


def embed_add_field(embed, title, content, inline=True):
    """Helper function to add an additional field to an embed"""
    embed.add_field(name=title, value=content, inline=inline)


def create_simple_embed(title, color, field_title, field_content):
    """Creates a simple embed with only 1 field"""
    embed = create_embed(title, color)
    embed_add_field(embed, field_title, field_content)
    return embed

def write_log(message):
    with open(f"./logs/{logname_file}.log", "a+") as f:
        f.write("\n"+message + "\n")
        f.close()
    print("[INFO]    Saved log")

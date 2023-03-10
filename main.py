import discord
from discord import app_commands
from discord.ext.commands import Greedy, Context
from typing import Optional
from discord.ext import commands
import util
import assets

# Setting variables
json_reader = util.load_json(assets.config_file)
url = json_reader["url"]
appid = json_reader["appid"]
token = json_reader["token"]
# Setting intents
intents = discord.Intents.default()
intents.message_content = True
from datetime import datetime
start_date = datetime.now()
start_date_pretty = start_date.strftime("%d/%m/%Y %H:%M:%S")
DEV_GUILD = discord.Object(id=1038431009676460082)

class sevenoseven(commands.Bot):
    def __init__(self, intents=intents):
        super().__init__(intents=intents, command_prefix=commands.when_mentioned, application_id = appid, description="707's official discord bot.")
    
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=DEV_GUILD)
    
    async def on_ready(self):
        print("[INFO]    Bot is starting...")
        for extension in assets.modules:
            await bot.load_extension(extension)
            util.write_log(f"Loaded {extension}")
            print(f"[INFO]    Loaded {extension}")
        print("[INFO]    Bot Loaded all extensions")
        await bot.change_presence(activity=discord.Game(name="Monitoring 707 cadets."))
        print("[INFO]    Bot custom status updated")
        print("[INFO]    Bot finished starting up!\n")
        print(f"[INFO]    Connected as: {bot.user}\n[INFO]    Invite URL: {url}\n[INFO]    Token: {token}")
        util.write_log(message=f"Bot started on {start_date_pretty}")

bot = sevenoseven(intents=intents)
bot.remove_command("help")

"""
*sync -> global sync
*sync guild -> sync current guild
*sync copy -> copies all global app commands to current guild and syncs
*sync delete -> clears all commands from the current guild target and syncs (removes guild commands)
*sync id_1 id_2 -> sync  guilds with 1 and 2
"""


@bot.command(name="synccmd")
@util.is_bot_admin()
async def sync(
        ctx: Context, guilds: Greedy[discord.Object], spec: Optional[str] = None) -> None:
    if not guilds:
        if spec == "guild":
            synced = await ctx.bot.tree.sync()
            util.write_log(f"{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator}) Synced commands to the current guild.")
        elif spec == "copy":
            ctx.bot.tree.copy_global_to(guild=DEV_GUILD)
            synced = await ctx.bot.tree.sync()
            util.write_log(f"{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator} Copied commands to the guild.)")
        elif spec == "delete":
            ctx.bot.tree.clear_commands()
            await ctx.bot.tree.sync()
            util.write_log(f"{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator}) Deleted commands from the current guild.")
            synced = []
        else:
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        print(
            f"[INFO]    Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1
    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    util.write_log(f"{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator} Synced commands globally.)")


bot.run(token)
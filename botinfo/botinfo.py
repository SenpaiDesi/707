import discord
from discord.ext import commands
from discord import app_commands
import platform
import time
import datetime
import util
up_time = time.time()
class botinfo(commands.Cog):
    """The commands used by devs."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="botinfo")
    async def botinfo(self, interaction : discord.Interaction):
        python_version = platform.python_version()
        python_build = platform.python_build()
        discord_version = discord.__version__
        ping = round(self.bot.latency * 1000)
        current_time = time.time()
        current_time_calculated = int(round(current_time - up_time))
        current_time_calculated_text = datetime.timedelta(seconds=current_time_calculated)
        embed = discord.Embed(title="Bot information", color = discord.Color.dark_gold())
        embed.add_field(name="Python Version", value=python_version, inline=False)
        embed.add_field(name="Python build:", value=python_build, inline=False)
        embed.add_field(name="Library version:", value=discord_version)
        embed.add_field(name="Latency", value=f"{ping} ms", inline=False)
        embed.add_field(name="Uptime", value= f"{current_time_calculated_text} DD/MM/SS")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        util.write_log(f"{interaction.user.id} ({interaction.user.name}#{interaction.user.discriminator}) invoked botinfo command.")

    @botinfo.error
    async def on_botinfo_error(self, interaction : discord.Interaction, error: app_commands.AppCommandError):
        python_version = platform.python_version()
        python_build = platform.python_build()
        discord_version = discord.__version__
        ping = round(self.bot.latency * 1000)
        current_time = time.time()
        current_time_calculated = int(round(current_time - up_time))
        current_time_calculated_text = datetime.timedelta(seconds=current_time_calculated)
        if isinstance(error, discord.errors.HTTPException):
            util.write_log(message=f"{datetime.datetime.utcnow()} Exception occured in botinfo {discord.errors.HTTPException}")
            await interaction.response.send_message(f"Python Version: {python_version}\nPython build: {python_build}\nLibrary version: {discord_version}\nLatency: {current_time_calculated_text}\nLatency: {ping}ms", ephemeral=True)
        elif isinstance(error, discord.errors.Forbidden):
            util.write_log(message=f"{datetime.datetime.utcnow()} Exception occured in botinfo {discord.errors.Forbidden}")
            await interaction.response.send_message(f"Python Version: {python_version}\nPython build: {python_build}\nLibrary version: {discord_version}\nLatency: {current_time_calculated_text}\nLatency: {ping}ms", ephemeral=True)
        else:
            await interaction.response.send_message(f"Something went wrong while loading information. Error code: `{error}`")
            util.write_log(f"{datetime.datetime.utcnow()} Exception occured in botinfo. {error}")
    

    @commands.Cog.listener()
    async def on_command(self, ctx):
        util.write_log(f"{ctx.command} Issued.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(botinfo(bot))
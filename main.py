# region Imports
import discord
from discord.ext import commands
import os
import configparser
# endregion

# region Variables
token = os.getenv("TOKEN")

intents = discord.Intents.all()
intents.members = True

config = configparser.ConfigParser()
config.read('config.ini')
prefix = config['MAIN']['Prefix']

bot = commands.Bot(prefix, intents=intents)
# endregion

# region Load cogs
initial_extensions = [

]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"[ + ] | Successfully loaded extension: | {extension}")
        except Exception as e:
            print(f"[ - ] | Failed to load extension:      | {extension}")
# endregion


@bot.event
async def on_ready():
    print("\n\n─────────────────────────────\n")
    bot_guilds = len(bot.guilds)
    bot_members = len(set(bot.get_all_members()))

    print(f"[ + ] | Logged in as:       | {bot.user}")
    print(f"[ + ] | User ID:            | {bot.user.id}")
    print(f"[ + ] | Guilds:             | {bot_guilds}")
    print(f"[ + ] | Members:            | {bot_guilds}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"))
    print(f"[ + ] | Discord.py Version: | {discord.__version__}")
    print("\n─────────────────────────────\n\n")

bot.run(token)

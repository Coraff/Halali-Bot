from dotenv import load_dotenv
import configparser
import os
from discord.ext import commands
import discord
# region Imports
# endregion
# region Variables
load_dotenv()
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


@commands.Cog.listener()
async def on_guild_join(self, guild: discord.Guild):
    logs = bot.get_channel(832393838400241705)

    await logs.send(f"Joined `{guild.name}`")


@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("─────────────────────────────\n")
    bot_guilds = len(bot.guilds)
    bot_members = len(set(bot.get_all_members()))

    print(f"[ + ] | Logged in as:       | {bot.user}")
    print(f"[ + ] | User ID:            | {bot.user.id}")
    print(f"[ + ] | Guilds:             | {bot_guilds}")
    print(f"[ + ] | Members:            | {bot_guilds}")
    print(f"[ + ] | Prefix:             | {prefix}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"))
    print(f"[ + ] | Discord.py Version: | {discord.__version__}")
    print("\n─────────────────────────────\n\n")

bot.run(token)

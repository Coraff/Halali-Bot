# region Imports
from dotenv import load_dotenv
import configparser
import os
from discord.ext import commands
import discord
import json
# endregion
# region Variables
load_dotenv()
token = os.getenv("TOKEN")

with open("vars.json") as f:
    vars = json.load(f)

intents = discord.Intents.all()
intents.members = True

config = configparser.ConfigParser()
config.read('config.ini')
prefix = config['MAIN']['Prefix']

bot = commands.Bot(prefix, intents=intents, case_insensitive=True)
bot.on_guild_join_log = config['OWNER']['Guild_Join_ID']
bot.restart_channel = vars[str("restart_channel")]
# endregion

# region Load cogs
initial_extensions = [
    'cogs.owner',
    'cogs.fun'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"[ + ] | Cog loaded:         | {extension}")
        except Exception as e:
            print(f"[ - ] | Cog failed to load: | {extension}")
# endregion


@bot.event
async def on_ready():
    #os.system('cls' if os.name == 'nt' else 'clear')
    print("\n─────────────────────────────\n")
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

    with open("vars.json", "r") as f:
        vars = json.load(f)

    if bot.restart_channel not in [0, "0"]:
        channel = bot.get_channel(bot.restart_channel)
        await channel.send("Bot has been restarted successfully.")

        vars["restart_channel"] = 0
        with open("vars.json", "w") as f:
            json.dump(vars, f)

bot.run(token)

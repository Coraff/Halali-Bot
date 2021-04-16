import discord
from discord.ext import commands
import random
import datetime
from datetime import datetime as DateTime
import os
import json
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import googletrans


class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_result = None
        self.trans = googletrans.Translator()

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command(hidden=True)
    async def translate(self, ctx, *, message: commands.clean_content):
        """Translates a message to English using Google translate."""

        loop = self.bot.loop

        try:
            ret = await loop.run_in_executor(None, self.trans.translate, message)
        except Exception as e:
            return await ctx.send(f'An error occurred: {e.__class__.__name__}: {e}')

        embed = discord.Embed(title='Translated', colour=0x4284F3)
        src = googletrans.LANGUAGES.get(ret.src, '(auto-detected)').title()
        dest = googletrans.LANGUAGES.get(ret.dest, 'Unknown').title()
        embed.add_field(name=f'From {src}', value=ret.origin, inline=False)
        embed.add_field(name=f'To {dest}', value=ret.text, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="Restart", aliases=["Reboot"], description="Restarts the bot.")
    async def restart(self, ctx: commands.Context):
        with open("vars.json", "r") as f:
            vars = json.load(f)

        vars["restart_channel"] = ctx.channel.id

        with open("vars.json", "w") as f:
            json.dump(vars, f)

        await ctx.send("Restarting... This may take some time")
        os.system('cls' if os.name == 'nt' else 'clear')
        os.system("python main.py")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        logs = self.bot.get_channel(int(self.bot.on_guild_join_log))

        if guild.system_channel:
            channel = guild.system_channel
        else:
            channel = random.choice(guild.channels)
        invite = await channel.create_invite(reason="Bot auto-join log")

        embed = discord.Embed()
        embed.color = 0x43B581
        embed.title = f"{guild.name}"
        embed.description = "────────────────"
        embed.url = invite.url
        embed.timestamp = DateTime.utcnow()

        embed.set_author(name="Joined server",
                         icon_url="https://cdn.discordapp.com/emojis/596576726163914752.png?v=1")

        embed.add_field(name="Member Count",
                        value=f"{guild.member_count} Members")
        embed.add_field(
            name="Owner", value=f"{guild.owner}\n{guild.owner.id}")

        embed.set_footer(
            text=f"Server ID: {guild.id}")

        await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        logs = self.bot.get_channel(int(self.bot.on_guild_join_log))

        embed = discord.Embed()
        embed.color = 0xD4342A
        embed.title = f"{guild.name}"
        embed.description = "────────────────"
        embed.timestamp = DateTime.utcnow()

        embed.set_author(name="Left server",
                         icon_url="https://cdn.discordapp.com/emojis/829245435625209886.png?v=1")

        embed.add_field(name="Member Count",
                        value=f"{guild.member_count} Members")
        embed.add_field(
            name="Owner", value=f"{guild.owner}\n{guild.owner.id}")

        embed.set_footer(
            text=f"Server ID: {guild.id}")

        await logs.send(embed=embed)

    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))

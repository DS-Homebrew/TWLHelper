#!/usr/bin/env python3

import discord
import settings

from discord.ext import commands
from utils.utils import create_error_embed


intents = discord.Intents.default()

cogs = [
    'cogs.general',
    'cogs.wiki',
    'cogs.load',
    'cogs.convert',
]


class embedHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page)
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
            await destination.send(embed=embed)


class TWLHelper(commands.Bot):
    def load_cogs(self):
        for cog in cogs:
            try:
                self.load_extension(cog)
                print(f"Loaded cog {cog}")
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                print("Failed to load cog {}\n{}".format(cog, exc))

    async def on_ready(self):
        print("TWLHelper ready.")

    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandInvokeError):
        author: discord.Member = ctx.author
        command: commands.Command = ctx.command or '<unknown cmd>'
        exc = getattr(exc, 'original', exc)
        channel = ctx.channel

        if isinstance(exc, commands.CommandNotFound):
            return

        elif isinstance(exc, commands.ArgumentParsingError):
            await ctx.send_help(ctx.command)

        elif isinstance(exc, commands.NoPrivateMessage):
            await ctx.send(f'`{command}` cannot be used in direct messages.')

        elif isinstance(exc, commands.MissingPermissions):
            await ctx.send(f"{author.mention} You don't have permission to use `{command}`.")

        elif isinstance(exc, commands.CheckFailure):
            await ctx.send(f'{author.mention} You cannot use `{command}`.')

        elif isinstance(exc, commands.BadArgument):
            await ctx.send(f'{author.mention} A bad argument was given: `{exc}`\n')
            await ctx.send_help(ctx.command)

        elif isinstance(exc, commands.BadUnionArgument):
            await ctx.send(f'{author.mention} A bad argument was given: `{exc}`\n')

        elif isinstance(exc, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention} You are missing required argument {exc.param.name}.\n')
            await ctx.send_help(ctx.command)

        elif isinstance(exc, discord.NotFound):
            await ctx.send("ID not found.")

        elif isinstance(exc, discord.Forbidden):
            await ctx.send(f"💢 I can't help you if you don't let me!\n`{exc.text}`.")

        elif isinstance(exc, commands.CommandInvokeError):
            await ctx.send(f'{author.mention} `{command}` raised an exception during usage')
            embed = create_error_embed(ctx, exc)
            await channel.send(embed=embed)
        else:
            await ctx.send(f'{author.mention} Unexpected exception occurred while using the command `{command}`')
            embed = create_error_embed(ctx, exc)
            await channel.send(embed=embed)


def main():
    intents = discord.Intents(guilds=True, members=True, bans=True, messages=True)

    bot = TWLHelper(settings.PREFIX, description="TWLHelper, DS⁽ⁱ⁾ Mode Hacking Discord server bot",
                    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False), intents=intents,
                    case_insensitive=True, status=discord.Status.online, activity=discord.Game(settings.STATUS))
    bot.help_command = embedHelp()
    print('Starting TWLHelper...')
    bot.load_cogs()
    bot.run(settings.TOKEN)

    return bot.exitcode


if __name__ == '__main__':
    exit(main())

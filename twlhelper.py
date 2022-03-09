#!/usr/bin/env python3

#
# ISC License
#
# Copyright (C) 2021-present DS-Homebrew
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import os
import discord
import gspread
import aiohttp
import settings

from shutil import rmtree
from discord.ext import commands
from utils.utils import create_error_embed


intents = discord.Intents.default()


class embedHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page)
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
            await destination.send(embed=embed)


class TWLHelper(commands.Bot):
    def __init__(self, command_prefix, description):
        intents = discord.Intents(guilds=True, members=True, bans=True, messages=True, message_content=True)
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
        activity = discord.Game(settings.STATUS)
        status = discord.Status.online
        super().__init__(
            command_prefix=command_prefix,
            description=description,
            intents=intents,
            allowed_mentions=allowed_mentions,
            activity=activity,
            status=status,
            case_insensitive=True
        )
        self.session = aiohttp.ClientSession()
        if settings.GSPREADKEY is not None:
            self.gspread = gspread.service_account(filename=settings.GSPREADKEY)

    def load_cogs(self):
        cog = ""
        for filename in os.listdir("./cogs"):
            try:
                if filename.endswith(".py"):
                    cog = f"cogs.{filename[:-3]}"
                    self.load_extension(cog)
                    print(f"Loaded cog cogs.{filename[:-3]}")
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                print("Failed to load cog {}\n{}".format(cog, exc))
        try:
            cog = "jishaku"
            self.load_extension("jishaku")
            print("Loaded cog jishaku")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cog, exc))

    async def close(self):
        await self.session.close()
        await super().close()

    async def is_owner(self, user: discord.User):
        if settings.GUILD:
            g = self.get_guild(settings.GUILD)
            if g:
                member = g.get_member(user.id)
                if member and any(role.id in settings.staff_roles for role in member.roles):
                    return True
        return await super().is_owner(user)

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

        elif isinstance(exc, commands.BadLiteralArgument):
            await ctx.send(f'{author.mention} A bad argument was given, expected one of {", ".join(exc.literals)}')

        elif isinstance(exc, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention} You are missing required argument `{exc.param.name}`.\n')
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
    bot = TWLHelper(settings.PREFIX, description="TWLHelper, DS⁽ⁱ⁾ Mode Hacking Discord server bot")
    bot.help_command = embedHelp()
    print('Starting TWLHelper...')
    bot.load_cogs()
    bot.run(settings.TOKEN)


if __name__ == '__main__':
    for folder in ("downloads", "senpai_converted_downloads"):
        try:
            rmtree(folder)
        except FileNotFoundError:
            pass
    main()

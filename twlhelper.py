#!/usr/bin/env python3

#
# Copyright (C) 2021-2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#

import asyncio
import contextlib
import logging
import os
from shutil import rmtree
from typing import Any, Dict, Union

import aiohttp
import discord
import gspread
from discord.ext import commands

from settings import loadSettings
from utils.utils import create_error_embed

log = logging.getLogger("bot")


class EmbedHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page)
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
            await destination.send(embed=embed)


class TWLHelper(commands.Bot):
    session: aiohttp.ClientSession

    def __init__(self, settings: Dict[str, Any], description: str):
        intents = discord.Intents(guilds=True, members=True, bans=True, messages=True, message_content=True)
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
        activity = discord.Game(settings['STATUS'])
        status = discord.Status.online
        self.settings = settings
        super().__init__(
            command_prefix=settings['PREFIX'],
            help_command=EmbedHelp(),
            description=description,
            intents=intents,
            allowed_mentions=allowed_mentions,
            activity=activity,
            status=status,
            case_insensitive=True
        )
        if settings['GSPREADKEY'] is not None:
            self.gspread = gspread.service_account(filename=settings['GSPREADKEY'])
        else:
            log.warning("gspread key not found, disabling it")

    async def load_cogs(self):
        cog = ""
        for filename in os.listdir("./cogs"):
            try:
                if filename.endswith(".py"):
                    cog = f"cogs.{filename[:-3]}"
                    await self.load_extension(cog)
                    log.info(f"Loaded cog cogs.{filename[:-3]}")
            except Exception as e:
                log.exception(f"Failed to load cog {cog}\n{type(e).__name__}: {e}")
        try:
            await self.load_extension("jishaku")
            log.info("Loaded cog jishaku")
        except Exception as e:
            log.exception(f"Failed to load cog jishaku\n{type(e).__name__}", exc_info=e)

    async def close(self):
        await self.session.close()
        await super().close()

    async def is_owner(self, user: discord.User):
        if self.settings['GUILD']:
            g = self.get_guild(self.settings['GUILD'])
            if g:
                member = g.get_member(user.id)
                if member and any(role.id in self.settings['staff_roles'] for role in member.roles):
                    return True
        log.info("Guild staff roles not set, bot owner set to default")
        return await super().is_owner(user)

    async def on_ready(self):
        log.info("TWLHelper ready.")

    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandInvokeError):
        author = ctx.author
        command: Union[commands.Command, str] = ctx.command or '<unknown cmd>'
        exc = getattr(exc, 'original', exc)

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
            await ctx.send(f'{author.mention} You are missing required argument `{exc.param.name}`.')
            await ctx.send_help(ctx.command)

        elif isinstance(exc, discord.Forbidden):
            await ctx.send(f"💢 I can't help you if you don't let me!\n`{exc.text}`.")

        elif isinstance(exc, commands.CommandInvokeError):
            await ctx.send(f'{author.mention} `{command}` raised an exception during usage', embed=create_error_embed(exc, ctx=ctx))

        else:
            await ctx.send(f'{author.mention} Unexpected exception occurred while using the command `{command}`',
                           embed=create_error_embed(exc, ctx=ctx))


async def main():
    # bot.log
    discord.utils.setup_logging(handler=logging.FileHandler('bot.log', encoding='utf-8', mode='w'))
    # Stream Handler
    discord.utils.setup_logging()

    settings = loadSettings()
    bot = TWLHelper(settings, description="TWLHelper, DS⁽ⁱ⁾ Mode Hacking Discord server bot")
    print('Starting TWLHelper...')
    async with bot:
        await bot.load_cogs()
        bot.session = aiohttp.ClientSession()
        await bot.start(settings['TOKEN'])


if __name__ == '__main__':
    for folder in ("downloads", "senpai_converted_downloads"):
        with contextlib.suppress(FileNotFoundError):
            rmtree(folder)
    asyncio.run(main())

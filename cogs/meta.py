#
# Copyright (C) 2015-2022 Rapptz
#
# SPDX-License-Identifier: MPL-2.0
#

import os
from inspect import getsourcefile, getsourcelines
from typing import Optional

import discord
from discord.ext import commands


class Meta(commands.Cog):
    """Bot meta"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=["botinfo", "whoisthisbot"])
    async def about(self, ctx):
        """About TWLHelper"""
        embed = discord.Embed(title="About TWLHelper")
        embed.set_author(name="DS-Homebrew")
        embed.url = "https://github.com/DS-Homebrew/TWLHelper"
        embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/TWLHelper/main/assets/TWLHelper.png")
        embed.description = "TWLHelper, DS⁽ⁱ⁾ Mode Hacking Discord server bot"
        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx, *, command: Optional[str] = None):
        """
        Gets the source code for a command
        """
        source_url = 'https://github.com/DS-Homebrew/TWLHelper'
        branch = 'main'
        if command is None:
            return await ctx.send(source_url)

        if command == 'help':
            src = type(self.bot.help_command)
            module = src.__module__
            filename = getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace('.', ' '))
            if obj is None:
                return await ctx.send('Could not find command.')

            # since we found the command we're looking for, presumably anyway, let's
            # try to access the code itself
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = getsourcelines(src)
        if not module.startswith('discord'):
            # not a built-in command
            location = os.path.relpath(filename).replace('\\', '/')  # type: ignore
        else:
            location = module.replace('.', '/') + '.py'
            source_url = 'https://github.com/Rapptz/discord.py'
            branch = 'master'

        final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'
        await ctx.send(final_url)


async def setup(bot):
    await bot.add_cog(Meta(bot))

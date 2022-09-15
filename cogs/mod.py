#
# Copyright (C) 2021-2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#

import discord
from discord.ext import commands
from utils import is_staff, create_error_embed


class Mod(commands.Cog):
    """
    Moderator-only commands.
    """
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        return True

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        """Loads a Cog."""
        try:
            if module[0:7] != "cogs.":
                module = "cogs." + module
            await self.bot.load_extension(module)
            await ctx.send('✅ Extension loaded.')
        except Exception as e:
            await ctx.send(embed=create_error_embed(e, ctx=ctx))

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        """Unloads a Cog."""
        try:
            if module[0:7] != "cogs.":
                module = "cogs." + module
            await self.bot.unload_extension(module)
            await ctx.send('✅ Extension unloaded.')
        except Exception as e:
            await ctx.send(embed=create_error_embed(e, ctx=ctx))

    @commands.command(name='reload')
    @commands.is_owner()
    async def reload(self, ctx, *, module: str):
        """Reloads a Cog."""
        try:
            if module[0:7] != "cogs.":
                module = "cogs." + module
            await self.bot.reload_extension(module)
            await ctx.send('✅ Extension reloaded.')
        except Exception as e:
            await ctx.send(embed=create_error_embed(e, ctx=ctx))

    @commands.command()
    @commands.check_any(commands.is_owner(), is_staff())
    async def speak(self, ctx: commands.Context, channel: discord.TextChannel, *, text: str):
        await channel.send(text, allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))


async def setup(bot):
    await bot.add_cog(Mod(bot))

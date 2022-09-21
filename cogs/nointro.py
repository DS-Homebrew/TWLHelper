#
# Copyright (C) 2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from ..twlhelper import TWLHelper


class NoIntro(commands.Cog):
    """No-Intro database lookup commands"""

    def __init__(self, bot):
        self.bot: TWLHelper = bot
        self.nitree = ET.parse('no-intro.dat')
        self.niroot = self.nitree.getroot()

    @commands.command()
    async def nicompare(self, ctx, gamecode: str, sha1hash: str):
        """
        Compares input ROM and hash against No-Intro.
        At the moment, only SHA1 comparison is supported.

        Usage:
            .nicompare <gamecode> <sha1hash>
        """
        for child in self.niroot:
            # skip the database header
            if child.tag == "header":
                continue
            if "serial" not in child[1].attrib:
                continue
            if child[1].attrib["serial"] == gamecode.upper():
                if child[1].attrib['sha1'] == sha1hash:
                    return await ctx.send("This ROM is valid.")
                else:
                    return await ctx.send("This ROM is invalid. This may mean that you may have trimmed this ROM, the ROM is corrupt, or it is a ROM hack.")
        await ctx.send("ROM not found. Is the game code correct?")


async def setup(bot):
    await bot.add_cog(NoIntro(bot))

#
# Copyright (C) 2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any, Optional, TYPE_CHECKING

import discord
from discord.ext import commands
from rapidfuzz import process

from utils import ViewPages

if TYPE_CHECKING:
    from ..twlhelper import TWLHelper


class NoIntroMenu(ViewPages):
    async def format_page(self, entry: Any):
        embed = discord.Embed()
        embed.title = f"{entry.attrib['name']} ({entry[1].attrib['serial']})"
        embed.add_field(name="Status", value=f"{entry[1].attrib['status'] if 'status' in entry[1].attrib else 'unverified'}", inline=False)
        embed.add_field(name="CRC32", value=f"{entry[1].attrib['crc']}", inline=False)
        embed.add_field(name="MD5", value=f"{entry[1].attrib['md5']}", inline=False)
        embed.add_field(name="SHA1", value=f"{entry[1].attrib['sha1']}", inline=False)
        if "sha256" in entry[1].attrib:
            embed.add_field(name="SHA256", value=f"{entry[1].attrib['sha256']}", inline=False)
        return embed


class NoIntro(commands.Cog):
    """No-Intro database lookup commands"""

    def __init__(self, bot):
        self.bot: TWLHelper = bot
        if self.bot.settings["NOINTRO"] is not None:
            self.nitree = ET.parse('no-intro.dat')
            self.niroot = self.nitree.getroot()

    async def cog_check(self, ctx):
        if self.bot.settings["NOINTRO"] is None:
            raise commands.CheckFailure()
        return True

    @commands.command()
    async def nicompare(self, ctx, gamecode: str, sha1hash: str):
        """
        Compares input ROM and hash against No-Intro.
        At the moment, only SHA1 comparison is supported.

        Usage:
            .nicompare <gamecode> <sha1hash>
        """
        sha1list = []
        for child in self.niroot:
            # skip the database header
            if child.tag == "header":
                continue
            if "serial" not in child[1].attrib:
                continue
            if child[1].attrib["serial"] == gamecode.upper():
                if "sha1" in child[1].attrib:
                    sha1list.append(child[1].attrib["sha1"])
        if not sha1list:
            return await ctx.send("ROM not found. Is the game code correct?")
        if sha1hash in sha1list:
            return await ctx.send("This ROM is valid.")
        else:
            return await ctx.send("This ROM is invalid. This may mean that you may have trimmed this ROM, the ROM is corrupt, or it is a ROM hack.")

    def getGameValues(self, name):
        for child in self.niroot:
            if child.tag == "header":
                continue
            if child.attrib["name"] == name:
                return child
        return None

    def search_tid(self, arg):
        gamelist = []
        for child in self.niroot:
            if child.tag == "header":
                continue
            if "serial" not in child[1].attrib:
                continue
            if child[1].attrib["serial"] == arg.upper():
                gamelist.append(child)
        return gamelist

    # This function is based on UDB-API, licensed Apache-2.0.
    # https://github.com/LightSage/UDB-API
    def search_name(self, arg):
        matchlist = []
        game_names = [child.attrib["name"] for child in self.niroot if "name" in child.attrib]
        results = process.extract(arg, [g.lower() for g in game_names], processor=lambda a: a.lower())
        for _, score, idx in results:
            if score < 70:
                continue
            game = self.getGameValues(game_names[idx])
            matchlist.append(game)
        return matchlist

    @commands.command(usage="[title id|game name]")
    async def nilookup(self, ctx, *, title: Optional[str]):
        """
        Shows a No-Intro database entry.
        Displays an embed with a link to the DAT-o-MATIC website if no arguments provided.
        """
        if not title:
            embed = discord.Embed()
            embed.title = "DAT-o-MATIC"
            embed.set_author(name="No-Intro")
            embed.description = "Database of all ROM dumps"
            embed.url = "https://datomatic.no-intro.org"
            return await ctx.send(embed=embed)

        tid = len(title) == 4
        if tid and title[0].upper() in ['H', 'Z', 'K']:
            return await ctx.send("DSiWare compatibility is not supported. Please try another game, or visit DAT-o-MATIC directly.")
        source = self.search_tid(title) if tid else self.search_name(title)
        if source:
            menu = NoIntroMenu(source, ctx)
            return await menu.start()
        else:
            await ctx.send("Game not found. Please try again.")


async def setup(bot):
    await bot.add_cog(NoIntro(bot))

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
from typing import Optional

import discord
import functools
import json
import settings

from rapidfuzz import process
from discord.ext import tasks, commands


class NBCompat(commands.Cog):
    """nds-bootstrap Compatibility API"""

    def __init__(self, bot):
        self.bot = bot
        self.loop.start()

    def cog_unload(self):
        self.loop.cancel()

    async def cog_check(self, ctx):
        if settings.GSPREADKEY is None:
            raise commands.CheckFailure()
        return True

    @tasks.loop(seconds=3600)
    async def loop(self):
        await self.bot.wait_until_ready()
        if settings.GSPREADKEY:
            await self.asyncDumpWorksheet()

    def dumpWorksheet(self):
        compatlist = self.bot.gspread.open_by_key('1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc')
        retailds = compatlist.worksheet("Retail ROMs (DSi/3DS)")
        testingqueue = compatlist.worksheet("Testing Queue")
        spreadsheet = retailds.get_all_values()
        if spreadsheet is None:
            return
        f = open("nbcompat.json", "w")
        json.dump(spreadsheet, f)
        f.close()
        spreadsheet = testingqueue.get_all_values()
        if spreadsheet is None:
            return
        f = open("nbcompat-fallback.json", "w")
        json.dump(spreadsheet, f)
        f.close()

    async def asyncDumpWorksheet(self):
        argv = functools.partial(self.dumpWorksheet)
        await self.bot.loop.run_in_executor(None, argv)

    def getGameValues(self, name, compatlist):
        for line in compatlist:
            if name == line[1]:
                return line
        return None

    # This function is based on UDB-API, licensed Apache-2.0.
    # https://github.com/LightSage/UDB-API
    def search_name(self, arg, compatlist):
        matchlist = []
        game_names = [line[1] for line in compatlist[2:]]
        results = process.extract(arg, [g.lower() for g in game_names], processor=lambda a: a.lower())
        for _, score, idx in results:
            if score < 70:
                continue
            game = self.getGameValues(game_names[idx], compatlist)
            matchlist.append([score, game])
        if matchlist:
            return matchlist[0][1]
        return None

    def search_tid(self, arg, compatlist):
        for line in compatlist[2:]:
            if arg.upper() in line[3]:
                return line
        return None

    @commands.command(aliases=["nbcompat", "ndscompat"], usage="[title id|game name]")
    async def ndsbcompat(self, ctx, *, title: Optional[str]):
        """
        Shows an nds-bootstrap compatibility list entry.
        Displays an embed with a link to the compatibility list if no arguments provided.
        """
        embed = discord.Embed()
        if not title:
            embed.title = "nds-bootstrap Compatibility List"
            embed.set_author(name="DS-Homebrew")
            embed.description = "Spreadsheet with all documented compatibility ratings for nds-bootstrap"
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
            embed.url = "https://docs.google.com/spreadsheets/d/1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc/edit?usp=sharing"
            await ctx.send(embed=embed)
            return

        game = None
        tid = len(title) == 4
        if tid and title[0] in ['H', 'Z', 'K']:
            return await ctx.send("DSiWare compatibility is not supported. Please try another game, or visit the list directly.")
        with open("nbcompat.json", "r") as compatfile:
            compatlist = json.load(compatfile)
        if tid:
            game = self.search_tid(title, compatlist)
        else:
            game = self.search_name(title, compatlist)
        if game:
            embed.title = f"{game[1]} ({game[4]})"
            embed.add_field(name="Last tested version", value=f"{game[10]}", inline=False)
            embed.add_field(name="Compatibility", value=f"{game[13]}", inline=False)
            if game[14] != '':
                embed.add_field(name="Notes", value=f"{game[14]}", inline=False)
        if embed:
            return await ctx.send(content=None, embed=embed)
        with open("nbcompat-fallback.json") as compatfile:
            compatlist = json.load(compatfile)
        if tid:
            game = self.search_tid(title, compatlist)
        else:
            game = self.search_name(title, compatlist)
        if game:
            return await ctx.send(f"{game[1]} ({game[4]}) does not have any compatibility ratings!")
        await ctx.send("Game not found. Please try again.")


def setup(bot):
    bot.add_cog(NBCompat(bot))

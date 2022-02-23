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

import discord
import functools
import json
import settings

from discord.ext import tasks, commands


class NBCompat(commands.Cog):
    """nds-bootstrap Compatibility API"""

    def __init__(self, bot):
        self.bot = bot
        self.loop.start()

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
        f = open("nbcompat.json", "w")
        json.dump(spreadsheet, f)
        f.close()
        spreadsheet = testingqueue.get_all_values()
        f = open("nbcompat-fallback.json", "w")
        json.dump(spreadsheet, f)
        f.close()

    async def asyncDumpWorksheet(self):
        argv = functools.partial(self.dumpWorksheet)
        await self.bot.loop.run_in_executor(None, argv)

    @commands.command(aliases=["nbcompat", "ndscompat"])
    async def ndsbcompat(self, ctx, tid=""):
        """Searching nds-bootstrap compatibility list\n
        Usage: .ndsbcompat [Title ID]"""
        embed = None
        if tid == "":
            embed = discord.Embed(title="nds-bootstrap Compatibility List")
            embed.set_author(name="DS-Homebrew")
            embed.description = "Spreadsheet with all documented compatibility ratings for nds-bootstrap"
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
            embed.url = "https://docs.google.com/spreadsheets/d/1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc/edit?usp=sharing"
            return await ctx.send(embed=embed)
        elif tid[0] == 'H' or tid[0] == 'Z' or tid[0] == 'K':
            return await ctx.send("DSiWare compatibility is not supported. Please try another game, or visit the list directly.")
        compatfile = open("nbcompat.json", "r")
        compatlist = json.load(compatfile)
        compatfile.close()
        for line in compatlist:
            if tid.upper() in line[3]:
                embed = discord.Embed()
                embed.title = f"{line[1]} ({line[4]})"
                embed.add_field(name="Last tested version", value=f"{line[10]}", inline=False)
                embed.add_field(name="Compatibility", value=f"{line[13]}", inline=False)
                if line[14] != '':
                    embed.add_field(name="Notes", value=f"{line[14]}", inline=False)
                break
        if embed:
            return await ctx.send(content=None, embed=embed)
        compatfile = open("nbcompat-fallback.json")
        compatlist = json.load(compatfile)
        compatfile.close()
        for line in compatlist:
            if tid.upper() in line[3]:
                return await ctx.send(f"{line[1]} ({line[4]}) does not have any compatibility ratings!")
        await ctx.send(f"{tid} not found. Please try again.")


def setup(bot):
    bot.add_cog(NBCompat(bot))

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
        compatlist = self.bot.gspread.open_by_key('1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc').worksheet("Retail ROMs (DSi/3DS)")
        spreadsheet = compatlist.get_all_values()
        f = open("nbcompat.json", "w")
        json.dump(spreadsheet, f)
        f.close()

    async def asyncDumpWorksheet(self):
        argv = functools.partial(self.dumpWorksheet)
        await self.bot.loop.run_in_executor(None, argv)

    @commands.command()
    async def ndsbcompat(self, ctx, tid=""):
        if tid == "":
            return await ctx.send("Please input a title key and try again.")
        compatfile = open("nbcompat.json", "r", encoding='utf-8')
        compatlist = json.load(compatfile)
        compatfile.close()
        embed = None
        for line in compatlist:
            if line[3] == tid:
                embed = discord.Embed()
                embed.title = f"{line[1]} ({line[4]})"
                embed.add_field(name="Last tested version", value=f"{line[10]}", inline=False)
                embed.add_field(name="Compatibility", value=f"{line[13]}", inline=False)
                if line[14] != '':
                    embed.add_field(name="Notes", value=f"{line[14]}", inline=False)
        if not embed:
            return await ctx.send(f"{tid} not found. Please try again.")
        return await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(NBCompat(bot))

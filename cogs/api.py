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

import json
import functools
import discord
import settings

from urllib import parse
from typing import Optional
from datetime import datetime
from pytz import timezone
from rapidfuzz import process
from discord.ext import tasks, commands
from utils import web_name


class API(commands.Cog):
    """Commands that access any API of sorts"""

    def __init__(self, bot):
        self.bot = bot
        self.loop.start()

    def cog_unload(self):
        self.loop.cancel()

    def gspreadkey_exists():
        def predicate(ctx):
            return settings.GSPREADKEY is not None
        return commands.check(predicate)

    @tasks.loop(hours=1)
    async def loop(self):
        await self.bot.wait_until_ready()
        await self.update_netinfo()
        if settings.GSPREADKEY:
            await self.asyncDumpWorksheet()

    # nds-bootstrap Compatibility list searching
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

    def search_tid(self, arg, compatlist, getlink=False):
        for idx, val in enumerate(compatlist[2:]):
            if arg.upper() in val[3]:
                if not getlink:
                    return val
                else:
                    # +1 because sheet starts from 1, but list starts from 0
                    # +2 added since searching starts from row 3
                    return idx + 3
        return None

    @commands.command(aliases=["nbcompat", "ndscompat"], usage="[title id|game name]")
    @gspreadkey_exists()
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
            game = self.search_tid(title, compatlist, getlink=False)
        else:
            game = self.search_name(title, compatlist)
        if game:
            embed.title = f"{game[1]} ({game[4]})"
            embed.add_field(name="Last tested version", value=f"{game[10]}", inline=False)
            embed.add_field(name="Compatibility", value=f"{game[13]}", inline=False)
            if game[14] != '':
                embed.add_field(name="Notes", value=f"{game[14]}", inline=False)
            gameidx = self.search_tid(game[3], compatlist, getlink=True)
            embed.add_field(name="Link", value=f"https://docs.google.com/spreadsheets/d/1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc/edit#gid=0&range=A{gameidx}:P{gameidx}", inline=False)
        if embed:
            return await ctx.send(content=None, embed=embed)
        with open("nbcompat-fallback.json") as compatfile:
            compatlist = json.load(compatfile)
        if tid:
            game = self.search_tid(title, compatlist, getlink=False)
        else:
            game = self.search_name(title, compatlist)
        if game:
            return await ctx.send(f"{game[1]} ({game[4]}) does not have any compatibility ratings!")
        await ctx.send("Game not found. Please try again.")

    # Nintendo Network status information
    # All netinfo related functions are based on Kurisu, licensed Apache-2.0.
    # https://github.com/nh-server/Kurisu
    netinfo_embed = discord.Embed(description="The Network Maintenance Information page has not been successfully checked yet.")

    def netinfo_parse_time(self, timestr):
        # netinfo is US/Pacific. Convert it to UTC so Discord timestamp works
        return timezone('US/Pacific').localize(datetime.strptime(' '.join(timestr.split()), '%A, %B %d, %Y %I :%M %p')).astimezone(timezone('UTC'))

    async def update_netinfo(self):
        async with self.bot.session.get('https://www.nintendo.co.jp/netinfo/en_US/status.json?callback=getJSON', timeout=45) as r:
            if r.status == 200:
                j = await r.json()
            else:
                self.netinfo_embed.description = "Failure when checking the Network Maintenance Information page."
                return

        now = datetime.now(timezone('US/Pacific'))

        embed = discord.Embed(title="Network Maintenance Information / Online Status",
                              url="https://www.nintendo.co.jp/netinfo/en_US/index.html",
                              timestamp=now)
        embed.set_footer(text="This information was last updated:")

        for status_type in ("operational_statuses", "temporary_maintenances"):
            descriptor = "Maintenance" if status_type == "temporary_maintenances" else "Status"

            for entry in j[status_type]:
                if "platform" in entry:
                    entry_desc = ', '.join(entry["platform"]).replace("nintendo", "Nintendo").replace("web", "Web")
                else:
                    entry_desc = 'No console specified.'

                begin = datetime(year=2000, month=1, day=1, tzinfo=timezone('US/Pacific'))
                end = datetime(year=2099, month=1, day=1, tzinfo=timezone('US/Pacific'))
                if "begin" in entry:
                    begin = self.netinfo_parse_time(entry["begin"])
                    entry_desc += f"\nBegins: {discord.utils.format_dt(begin, style='F')}"
                if "end" in entry:
                    end = self.netinfo_parse_time(entry["end"])
                    entry_desc += f"\nEnds: {discord.utils.format_dt(end, style='F')}"

                if now < end:
                    entry_name = "{} {}: {}".format(
                        "Current" if begin <= now else "Upcoming",
                        descriptor,
                        entry["software_title"].replace(' <br />\r\n', ', ')
                    )
                    if "services" in entry:
                        entry_name += ", " + ', '.join(entry["services"])
                    embed.add_field(name=entry_name, value=entry_desc, inline=False)
        if len(embed.fields) == 0:
            embed.description = "No ongoing or upcoming maintenances."
        self.netinfo_embed = embed

    @commands.command()
    async def netinfo(self, ctx):
        """Shows the Nintendo Network status information"""
        await ctx.send(embed=self.netinfo_embed)

    # UniStore related functions
    def uniembed(self, embed, appid, store):
        embed.title = appid["title"]
        embed.color = int(appid['color'][1:], 16) if 'color' in appid else None
        embed.set_author(name=appid["author"], icon_url=appid["avatar"] if "avatar" in appid else None)
        embed.set_thumbnail(url=appid["icon"] if "icon" in appid else (appid["image"] if "image" in appid else (appid["avatar"] if "avatar" in appid else None)))
        embed.description = appid["description"] if "description" in appid else None
        if store == "udb":
            embed.url += appid["systems"][0].lower() + "/"
        embed.url += web_name(appid["title"])
        return embed

    async def udbparse(self, ctx, search="", israndom=False):
        app = None
        r = None

        async with ctx.typing():
            if israndom or search != "":
                if israndom:
                    r = await self.bot.session.get("https://udb-api.lightsage.dev/random")
                elif search != "":
                    r = await self.bot.session.get(f"https://udb-api.lightsage.dev/search/{search}")
                if r.status == 200:
                    app = await r.json()
                elif r.status == 422:
                    return await ctx.send("HTTP 422: Validation error. Please try again later.")
                else:
                    return await ctx.send("Unknown response from API. Please try again later.")
            embed = discord.Embed(title="Universal-DB", colour=0x1d8056)
            embed.url = "https://db.universal-team.net/"
            if israndom:
                return await ctx.send(embed=self.uniembed(embed, app[0], "udb"))
            elif search != "":
                if app["results"]:
                    return await ctx.send(embed=self.uniembed(embed, app["results"][0], "udb"))
                else:
                    return await ctx.send("App cannot be found. Please try again.")
            # when no args
            embed.set_author(name="Universal-Team")
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/49733679?s=400&v=4")
            embed.description = "A database of DS and 3DS homebrew"
            await ctx.send(embed=embed)

    async def skinparse(self, ctx, title, extension, skin="", israndom=False):
        item = None
        r = None

        async with ctx.typing():
            if skin != "" or israndom:
                if israndom:
                    r = await self.bot.session.get(f"https://twlmenu-extras.api.hansol.ca/random/{extension}")
                elif skin != "":
                    r = await self.bot.session.get(f"https://twlmenu-extras.api.hansol.ca/search/{extension}/{skin}")
                if r.status == 200:
                    item = await r.json()
                elif r.status == 422:
                    return await ctx.send("HTTP 422: Validation error. Please try again later.")
                else:
                    return await ctx.send("Unknown response from API. Please try again later.")
            embed = discord.Embed(title=title, colour=0xda4a53)
            embed.url = f"https://skins.ds-homebrew.com/{web_name(extension)}/"
            if israndom:
                return await ctx.send(embed=self.uniembed(embed, item[0], "skin"))
            elif skin != "":
                if item["results"]:
                    return await ctx.send(embed=self.uniembed(embed, item["results"][0], "skin"))
                else:
                    return await ctx.send("Skin cannot be found. Please try again.")
            # when no args
            embed.set_author(name="DS-Homebrew")
            if extension == "Unlaunch":
                embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
                embed.description = "Custom backgrounds for Unlaunch"
            elif extension == "Nintendo DSi":
                embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/dsi.png")
                embed.description = "Custom skins for TWiLight Menu++'s DSi Menu theme"
            elif extension == "R4 Original":
                embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/r4.png")
                embed.description = "Custom skins for TWiLight Menu++'s R4 Original Menu theme"
            elif extension == "Nintendo 3DS":
                embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/3ds.png")
                embed.description = "Custom skins for TWiLight Menu++'s 3DS Menu theme"
            elif extension == "Font":
                embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/font.png")
                embed.description = "Custom fonts for TWiLight Menu++"
            elif extension == "Icon":
                embed.description = "Custom icons for TWiLight Menu++"
            await ctx.send(embed=embed)

    @commands.command(aliases=["universaldb"])
    async def udb(self, ctx, *args):
        """Displays an embed with a link to Universal-DB and/or one of the apps.\n
        To show a random app: `udb [-r]`
        To search for an app: `udb [search parameter]`"""
        if args and args[0] == "-r":
            await self.udbparse(ctx, israndom=True)
        else:
            app = "".join(args)
            await self.udbparse(ctx, app)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def skins(self, ctx):
        """Displays an embed with a link to a database of TWiLight Menu++ skins and Unlaunch backgrounds\n
        To show a random skin: `skins [console] -r`
        To search for a skin: `skins [console] [search parameter]`"""
        embed = discord.Embed(title="Skins", colour=0xda4a53)
        embed.set_author(name="DS-Homebrew")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.description = "A collection of skins for TWiLight Menu++ from DS-Homebrew/twlmenu-extras on GitHub"
        embed.url = "https://skins.ds-homebrew.com/"
        await ctx.send(embed=embed)

    @skins.command(name="unlaunch")
    async def skin_unlaunch(self, ctx, *args):
        """Displays an embed with a link to the Unlaunch backgrounds page.\n
        To show a random background: `skins unlaunch [-r]`
        To search for a background: `skins unlaunch [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "Unlaunch Backgrounds", "Unlaunch", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "Unlaunch Backgrounds", "Unlaunch", skin)

    @skins.command(name="dsi", aliases=["dsimenu"])
    async def skin_dsimenu(self, ctx, *args):
        """Displays an embed with a link to the DSi Menu skins page.\n
        To show a random skin: `skins dsi [-r]`
        To search for a skin: `s`kins dsi [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "DSi Menu Skins", "Nintendo DSi", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "DSi Menu Skins", "Nintendo DSi", skin)

    @skins.command(name="3ds", aliases=["3dsmenu"])
    async def skin_3dsmenu(self, ctx, *args):
        """Displays an embed with a link to the 3DS Menu skins page.\n
        To show a random skin: `skins 3ds [-r]`
        To search for a skin: `skins 3ds [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "3DS Menu Skins", "Nintendo 3DS", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "3DS Menu Skins", "Nintendo 3DS", skin)

    @skins.command(name="r4", aliases=["r4theme"])
    async def skin_r4menu(self, ctx, *args):
        """Displays an embed with a link to the R4 Original Menu skins page.\n
        To show a random skin: `skins r4 [-r]`
        To search for a skin: `skins r4 [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "R4 Original Menu Skins", "R4 Original", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "R4 Original Menu Skins", "R4 Original", skin)

    @skins.command(name="font")
    async def skin_font(self, ctx, *args):
        """Displays an embed with a link to the TWiLight Menu++ fonts page.\n
        To show a random font: `skins fonts [-r]`
        To search for a font: `skins fonts [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "TWiLight Menu++ Fonts", "Font", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "TWiLight Menu++ Fonts", "Font", skin)

    @skins.command(name="icon")
    async def skin_icon(self, ctx, *args):
        """Displays an embed with a link to the TWiLight Menu++ icons page.\n
        To show a random icon: `skins icon [-r]`
        To search for an icon: `skins icon [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "TWiLight Menu++ Icons", "Icon", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "TWiLight Menu++ Icons", "Icon", skin)

    # Gamebrew searching
    @commands.command()
    async def gamebrew(self, ctx, *args):
        """Searches for an app on GameBrew"""
        if not args:
            embed = discord.Embed()
            embed.title = "GameBrew"
            embed.description = "A wiki dedicated to Video Game Homebrew."
            embed.set_author(name="GameBrew", icon_url="https://www.gamebrew.org/images/logo3.png")
            embed.url = "https://www.gamebrew.org/wiki/Main_Page"
            return await ctx.send(embed=embed)

        async with ctx.typing():
            r = await self.bot.session.get(f"https://www.gamebrew.org/api.php?action=opensearch&limit=1&namespace=0&format=json&redirects=resolve&search={parse.quote(' '.join(args))}")
            if r.status != 200:
                return await ctx.send(f"Error {r.status}! Failed to connect to GameBrew API")

            apiData = await r.json()

            if len(apiData[1]) > 0:
                embed = discord.Embed()
                embed.title = apiData[1][0]
                embed.set_author(name="GameBrew", icon_url="https://www.gamebrew.org/images/logo3.png")
                embed.url = apiData[3][0]
                await ctx.send(embed=embed)
            else:
                await ctx.send("App cannot be found. Please try again.")


async def setup(bot):
    await bot.add_cog(API(bot))

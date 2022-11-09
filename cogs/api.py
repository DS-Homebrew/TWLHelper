#
# Copyright (C) 2021-2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#
from __future__ import annotations

import functools
import json
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from urllib import parse

import aiohttp
import discord
from discord.ext import commands, tasks
from pytz import timezone
from rapidfuzz import process
from re import findall

from utils import ViewPages, web_name

if TYPE_CHECKING:
    from twlhelper import TWLHelper


class UDBMenu(ViewPages):
    async def format_page(self, entry: Any):
        embed = discord.Embed(title=entry['title'], url=f'https://db.universal-team.net/{entry["systems"][0].lower()}/{(entry["slug"])}')
        embed.color = int(entry['color'][1:], 16) if 'color' in entry else None
        embed.set_author(name=entry["author"], icon_url=entry["avatar"] if "avatar" in entry else None)
        embed.set_thumbnail(url=entry["icon"] if "icon" in entry else (entry["image"] if "image" in entry else (entry["avatar"] if "avatar" in entry else None)))
        embed.description = entry["description"] if "description" in entry else None
        return embed


class SkinsMenu(ViewPages):
    async def format_page(self, entry: Any):
        store_name = web_name(self.ctx.command.extras['store'])
        embed = discord.Embed()
        embed.title = entry["title"]
        embed.color = int(entry['color'][1:], 16) if 'color' in entry else None
        embed.set_author(name=entry["author"], icon_url=entry["avatar"] if "avatar" in entry else None)
        embed.set_thumbnail(url=entry["icon"] if "icon" in entry else (entry["image"] if "image" in entry else (entry["avatar"] if "avatar" in entry else None)))
        embed.description = entry["description"] if "description" in entry else None
        embed.url = f'https://skins.ds-homebrew.com/{store_name}/{web_name(entry["title"])}'
        return embed


class NBCompatMenu(ViewPages):
    async def format_page(self, entry: Any):
        embed = discord.Embed()
        embed.title = f"{entry[1]} ({entry[4]})"
        embed.add_field(name="Last tested version", value=f"{entry[10]}", inline=False)
        embed.add_field(name="Compatibility", value=f"{entry[13]}", inline=False)
        if entry[14] != '':
            embed.add_field(name="Notes", value=f"{entry[14]}", inline=False)
        embed.add_field(name="Link", value=f"{entry[16]}", inline=False)
        return embed


class GbatekMenu(ViewPages):
    async def format_page(self, link: Any):
        embed = discord.Embed(title=f"GBATEK – {link[1]}", url=f'https://problemkaputt.de/{link[0]}')
        embed.set_author(name="Nocash")
        embed.set_thumbnail(url="https://i.imgur.com/03jnZtC.png")
        return embed


class NetInfoManager(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.cog: API = ctx.cog  # type: ignore

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This view is not for you!", ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        await self.ctx.message.edit(view=None)

    @discord.ui.button(label="Refresh", emoji="\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}",
                       style=discord.ButtonStyle.blurple)
    async def refresh_button(self, itx: discord.Interaction, button: discord.ui.Button):
        try:
            await self.cog.update_netinfo()
        except Exception as e:
            await itx.response.send_message(f"An exception occurred refreshing netinfo:\n{e}", ephemeral=True)

        await itx.response.send_message("Refreshed netinfo!", ephemeral=True)
        await self.ctx.message.edit(embed=self.cog.netinfo_embed)


def gspreadkey_exists():
    def predicate(ctx):
        return ctx.bot.settings['GSPREADKEY'] is not None
    return commands.check(predicate)


class API(commands.Cog):
    """Commands that access any API of sorts"""

    def __init__(self, bot: TWLHelper):
        self.bot = bot
        if bot.settings['GSPREADKEY']:
            self.loop.start()

        # Netinfo
        self.netinfo_task.add_exception_type(aiohttp.ContentTypeError)
        self.netinfo_task.start()

    def cog_unload(self):
        self.netinfo_task.stop()
        self.loop.cancel()

    @tasks.loop(minutes=20)
    async def netinfo_task(self) -> None:
        await self.update_netinfo()

    @netinfo_task.before_loop
    async def before_netinfo_task(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=1)
    async def loop(self):
        await self.bot.wait_until_ready()
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

    def search_tid(self, arg, compatlist, getlink=False):
        for idx, val in enumerate(compatlist[2:]):
            if arg.upper() in val[3]:
                if not getlink:
                    game = val
                    game.append(f"https://docs.google.com/spreadsheets/d/1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc/edit#gid=0&range=A{idx+3}:P{idx+3}")
                    return [game]
                else:
                    # +1 because sheet starts from 1, but list starts from 0
                    # +2 added since searching starts from row 3
                    return f"https://docs.google.com/spreadsheets/d/1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc/edit#gid=0&range=A{idx+3}:P{idx+3}"
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
            game.append(self.search_tid(game[3], compatlist, getlink=True))
            matchlist.append(game)
        return matchlist

    @commands.command(aliases=["nbcompat", "ndscompat"], usage="[title id|game name]")
    @gspreadkey_exists()
    async def ndsbcompat(self, ctx, *, title: Optional[str]):
        """
        Shows an nds-bootstrap compatibility list entry.
        Displays an embed with a link to the compatibility list if no arguments provided.
        """
        if not title:
            embed = discord.Embed()
            embed.title = "nds-bootstrap Compatibility List"
            embed.set_author(name="DS-Homebrew")
            embed.description = "Spreadsheet with all documented compatibility ratings for nds-bootstrap"
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
            embed.url = "https://docs.google.com/spreadsheets/d/1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc/edit?usp=sharing"
            return await ctx.send(embed=embed)

        tid = len(title) == 4
        if tid and title[0].upper() in ['H', 'Z', 'K']:
            return await ctx.send("DSiWare compatibility is not supported. Please try another game, or visit the list directly.")
        with open("nbcompat.json", "r") as compatfile:
            compatlist = json.load(compatfile)
        source = self.search_tid(title, compatlist, getlink=False) if tid else self.search_name(title, compatlist)
        if source:
            menu = NBCompatMenu(source, ctx)
            return await menu.start()
        else:
            with open("nbcompat-fallback.json") as compatfile:
                compatlist = json.load(compatfile)
            source = self.search_tid(title, compatlist, getlink=False) if tid else self.search_name(title, compatlist)
            if source:
                return await ctx.send(f"{source[0][1]} ({source[0][4]}) does not have any compatibility ratings!")
            await ctx.send("Game not found. Please try again.")

    # Nintendo Network status information
    # All netinfo related functions are based on Kurisu, licensed Apache-2.0.
    # https://github.com/nh-server/Kurisu
    netinfo_embed = discord.Embed(description="The Network Maintenance Information page has not been successfully checked yet.")

    def netinfo_parse_time(self, timestr):
        # netinfo is US/Pacific. Convert it to UTC so Discord timestamp works
        return timezone('US/Pacific').localize(datetime.strptime(' '.join(timestr.split()), '%A, %B %d, %Y %I :%M %p')).astimezone(timezone('UTC'))

    async def update_netinfo(self):
        now = datetime.now(timezone('US/Pacific'))

        embed = discord.Embed(title="Network Maintenance Information / Online Status",
                              url="https://www.nintendo.co.jp/netinfo/en_US/index.html",
                              timestamp=now)
        embed.set_footer(text="This information was last fetched at")

        async with self.bot.session.get('https://www.nintendo.co.jp/netinfo/en_US/status.json?callback=getJSON', timeout=45) as r:
            if r.status == 200:
                # Nintendo likes to fuck up the json content type sometimes.
                j = await r.json(content_type=None)
            else:
                embed.description = "Failure when checking the Network Maintenance Information page."
                self.netinfo_embed = embed
                return

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
                if "end" in entry and entry["end"] is not None:
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
            embed.description = "No ongoing or upcoming maintenance."

        self.netinfo_embed = embed

    @commands.command()
    async def netinfo(self, ctx):
        """Shows the Nintendo Network status information"""
        if await self.bot.is_owner(ctx.author):
            view = NetInfoManager(ctx)
        else:
            view = None

        await ctx.send(embed=self.netinfo_embed, view=view)

    async def request(self, url: str):
        async with self.bot.session.get(url) as r:
            if r.status != 200:
                raise commands.CommandError(f"Unable to request the api for some reason. ({r.status})")
            return await r.json()

    @commands.command(aliases=["universaldb"])
    async def udb(self, ctx, *, application=None):
        """Displays an embed with a link to Universal-DB and/or one of the apps.\n
        To show a random app: `udb [-r]`
        To search for an app: `udb [search parameter]`"""
        if not application:
            embed = discord.Embed(title="Universal-DB", colour=0x1d8056)
            embed.url = "https://db.universal-team.net/"
            embed.set_author(name="Universal-Team")
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/49733679?s=400&v=4")
            embed.description = "A database of DS and 3DS homebrew"
            await ctx.send(embed=embed)
            return

        if application.strip() == "-r":
            url = "https://udb-api.lightsage.dev/random"
        else:
            url = f"https://udb-api.lightsage.dev/search/{parse.quote(application)}"
        resp = await self.request(url)
        source = resp['results'] if type(resp) == dict else resp
        if not source:
            return await ctx.send("App not found. Please try again.")

        menu = UDBMenu(source, ctx)
        await menu.start()

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

    async def send_skin_help(self, ctx: commands.Context):
        embed = discord.Embed(colour=0xda4a53)
        store_name = ctx.command.extras['store']
        embed.url = f"https://skins.ds-homebrew.com/{web_name(store_name)}/"
        embed.set_author(name="DS-Homebrew")
        if store_name == "Unlaunch":
            embed.title = "Unlaunch Backgrounds"
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
            embed.description = "Custom backgrounds for Unlaunch"
        elif store_name == "Nintendo DSi":
            embed.title = "DSi Menu Skins"
            embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/dsi.png")
            embed.description = "Custom skins for TWiLight Menu++'s DSi Menu theme"
        elif store_name == "R4 Original":
            embed.title = "R4 Original Menu Skins"
            embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/r4.png")
            embed.description = "Custom skins for TWiLight Menu++'s R4 Original Menu theme"
        elif store_name == "Nintendo 3DS":
            embed.title = "3DS Menu Skins"
            embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/3ds.png")
            embed.description = "Custom skins for TWiLight Menu++'s 3DS Menu theme"
        elif store_name == "Font":
            embed.title = "TWiLight Menu++ Fonts"
            embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/font.png")
            embed.description = "Custom fonts for TWiLight Menu++"
        elif store_name == "Icon":
            embed.title = "TWiLight Menu++ Icons"
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
            embed.description = "Custom icons for TWiLight Menu++"

        await ctx.send(embed=embed)

    async def start_skin_menu(self, ctx, argument):
        store_name = parse.quote(ctx.command.extras['store'])

        if argument.strip() == "-r":
            url = f"https://twlmenu-extras.api.hansol.ca/random/{store_name}"
        else:
            url = f"https://twlmenu-extras.api.hansol.ca/search/{store_name}/{parse.quote(argument)}"
        resp = await self.request(url)
        source = resp['results'] if type(resp) == dict else resp
        if not source:
            return await ctx.send("Skin not found. Please try again.")
        menu = SkinsMenu(source, ctx)
        await menu.start()

    @skins.command(name="unlaunch", extras={"store": "Unlaunch"})
    async def skin_unlaunch(self, ctx, *, skin=None):
        """Displays an embed with a link to the Unlaunch backgrounds page.

        To show a random background: `skins unlaunch [-r]`
        To search for a background: `skins unlaunch [search parameter]`"""
        if not skin:
            await self.send_skin_help(ctx)
            return

        await self.start_skin_menu(ctx, skin)

    @skins.command(name="dsi", aliases=["dsimenu"], extras={"store": "Nintendo DSi"})
    async def skin_dsimenu(self, ctx, *, skin=None):
        """Displays an embed with a link to the DSi Menu skins page.

        To show a random skin: `skins dsi [-r]`
        To search for a skin: `skins dsi [search parameter]`"""
        if not skin:
            await self.send_skin_help(ctx)
            return

        await self.start_skin_menu(ctx, skin)

    @skins.command(name="3ds", aliases=["3dsmenu"], extras={"store": "Nintendo 3DS"})
    async def skin_3dsmenu(self, ctx, *, skin=None):
        """Displays an embed with a link to the 3DS Menu skins page.

        To show a random skin: `skins 3ds [-r]`
        To search for a skin: `skins 3ds [search parameter]`"""
        if not skin:
            await self.send_skin_help(ctx)
            return

        await self.start_skin_menu(ctx, skin)

    @skins.command(name="r4", aliases=["r4theme"], extras={"store": "R4 Original"})
    async def skin_r4menu(self, ctx, *, skin=None):
        """Displays an embed with a link to the R4 Original Menu skins page.

        To show a random skin: `skins r4 [-r]`
        To search for a skin: `skins r4 [search parameter]`"""
        if not skin:
            await self.send_skin_help(ctx)
            return

        await self.start_skin_menu(ctx, skin)

    @skins.command(name="font", extras={"store": "Font"})
    async def skin_font(self, ctx, *, skin=None):
        """Displays an embed with a link to the TWiLight Menu++ fonts page.

        To show a random font: `skins fonts [-r]`
        To search for a font: `skins fonts [search parameter]`"""
        if not skin:
            await self.send_skin_help(ctx)
            return

        await self.start_skin_menu(ctx, skin)

    @skins.command(name="icon", extras={"store": "Icon"})
    async def skin_icon(self, ctx, *, skin=None):
        """Displays an embed with a link to the TWiLight Menu++ icons page.

        To show a random icon: `skins icon [-r]`
        To search for an icon: `skins icon [search parameter]`"""
        if not skin:
            await self.send_skin_help(ctx)
            return

        await self.start_skin_menu(ctx, skin)

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

    # GBATEK searching

    # This function is based on UDB-API, licensed Apache-2.0.
    # https://github.com/LightSage/UDB-API
    def search_link(self, query, list):
        matchlist = []
        results = process.extract(query.lower().strip(), [link[1].lower() for link in list])
        for _, score, idx in results:
            if score < 70:
                continue
            matchlist.append(list[idx])
        return matchlist

    @commands.command()
    async def gbatek(self, ctx, *, page):
        """Links to a page on GBATEK"""

        async with self.bot.session.get("https://problemkaputt.de/gbatek-index.htm") as r:
            if r.status == 200:
                content = await r.text()
                link_list = findall(r'<A HREF="([\w\-]+\.htm)">([^<]+)</A>', content)
            else:
                return await ctx.send("Error: Unable to access GBATEK")

        links = self.search_link(page, link_list)
        if not links:
            return await ctx.send("No pages found. Please try again.")

        menu = GbatekMenu(links, ctx)
        await menu.start()

    @commands.command(aliases=['mkey'])
    async def generatemkey(self, ctx, device: str, month: int, day: int, inquiry: str, deviceid: Optional[str] = None):
        """
        Generate an mkey for given device.
        Usage: `mkey <3ds|dsi|wii|wiiu|switch> <month> <day> <inquiry (no space)> <deviceid (switch 8.0+ only)>`
        """
        devices = {
            "3ds": "CTR",
            "dsi": "TWL",
            "wii": "RVL",
            "wiiu": "WUP",
            "ns": "HAC",
            "nx": "HAC",
            "switch": "HAC"
        }
        if deviceid:
            await ctx.message.delete()
        if device.lower() not in devices:
            return await ctx.send(f'{ctx.author.mention} This device is not supported. Valid options are: {", ".join(i for i in devices)}')
        apicall = f"https://mkey.eiphax.tech/api?platform={devices[device.lower()]}&inquiry={inquiry}&month={month}&day={day}"
        if deviceid:
            apicall += f"&aux={deviceid}"
        async with self.bot.session.get(apicall) as r:
            if r.status == 200:
                ret = await r.json()
                return await ctx.send(f'{ctx.author.mention} Your key is {ret["key"]}.')
            else:
                return await ctx.send(f'{ctx.author.mention} API returned error {r.status}. Please check your values and try again.')


async def setup(bot: TWLHelper):
    await bot.add_cog(API(bot))

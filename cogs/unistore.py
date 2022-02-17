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

from discord.ext import commands
from utils import web_name


class UniStore(commands.Cog):
    """Commands related to UniStore searching"""

    def __init__(self, bot):
        self.bot = bot

    def uniembed(self, embed, appid, store):
        embed.title = appid["title"]
        embed.color = int(appid['color'][1:], 16) if 'color' in appid else discord.Embed.Empty
        embed.set_author(name=appid["author"], icon_url=appid["avatar"] if "avatar" in appid else discord.Embed.Empty)
        embed.set_thumbnail(url=appid["icon"] if "icon" in appid else (appid["image"] if "image" in appid else (appid["avatar"] if "avatar" in appid else discord.Embed.Empty)))
        embed.description = appid["description"] if "description" in appid else discord.Embed.Empty
        if store == "udb":
            embed.url += appid["systems"][0].lower() + "/"
        embed.url += web_name(appid["title"])
        return embed

    async def udbparse(self, ctx, search="", israndom=False):
        app = None
        r = None
        if israndom or search != "":
            if israndom:
                r = await self.bot.session.get("https://udb-api.lightsage.dev/random")
            elif search != "":
                r = await self.bot.session.get("https://udb-api.lightsage.dev/search/" + search)
            if r.status == 200:
                app = await r.json()
            elif r.status == 422:
                return await ctx.send("HTTP 422: Validation error. Please try again later.")
            else:
                return await ctx.send("Unknown response from API. Please try again later.")
        embed = discord.Embed(title="Universal-DB", colour=discord.Colour.from_rgb(7, 47, 79))
        embed.set_author(name="Universal-Team")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/49733679?s=400&v=4")
        embed.description = "A database of DS and 3DS homebrew"
        embed.url = "https://db.universal-team.net/"
        if israndom:
            return await ctx.send(embed=self.uniembed(embed, app[0], "udb"))
        if search != "":
            if app["results"]:
                return await ctx.send(embed=self.uniembed(embed, app["results"][0], "udb"))
            return await ctx.send("App cannot be found. Please try again.")
        await ctx.send(embed=embed)

    async def skinparse(self, ctx, title, extension, skin="", israndom=False):
        item = None
        r = None
        if skin != "" or israndom:
            if israndom:
                r = await self.bot.session.get("https://twlmenu-extras.api.hansol.ca/random/" + extension)
            elif skin != "":
                r = await self.bot.session.get("https://twlmenu-extras.api.hansol.ca/search/" + extension + "/" + skin)
            if r.status == 200:
                item = await r.json()
            elif r.status == 422:
                return await ctx.send("HTTP 422: Validation error. Please try again later.")
            else:
                return await ctx.send("Unknown response from API. Please try again later.")
        embed = discord.Embed(title=title)
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
        embed.url = "https://skins.ds-homebrew.com/" + web_name(extension) + "/"
        if israndom:
            return await ctx.send(embed=self.uniembed(embed, item[0], "skin"))
        if skin != "":
            if item["results"]:
                return await ctx.send(embed=self.uniembed(embed, item["results"][0], "skin"))
            return await ctx.send("Skin cannot be found. Please try again.")
        await ctx.send(embed=embed)

    @commands.command(aliases=["universaldb"])
    async def udb(self, ctx, *args):
        """Links to Universal-DB and/or one of the apps.\n
        To show a random app: `udb [-r]`
        To search for an app: `udb [search parameter]`"""
        if args and args[0] == "-r":
            await self.udbparse(ctx, israndom=True)
        else:
            app = "".join(args)
            await self.udbparse(ctx, app)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def skins(self, ctx):
        """Links to a database of TWiLight Menu++ skins and Unlaunch backgrounds\n
        To show a random skin: `skins [console] -r`
        To search for a skin: `skins [console] [search parameter]`"""
        embed = discord.Embed(title="Skins")
        embed.set_author(name="DS-Homebrew")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.description = "A collection of skins for TWiLight Menu++ from DS-Homebrew/twlmenu-extras on GitHub"
        embed.url = "https://skins.ds-homebrew.com/"
        await ctx.send(embed=embed)

    @skins.command(name="unlaunch")
    async def skin_unlaunch(self, ctx, *args):
        """Links to the Unlaunch backgrounds page.\n
        To show a random background: `skins unlaunch [-r]`
        To search for a background: `skins unlaunch [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "Unlaunch Backgrounds", "Unlaunch", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "Unlaunch Backgrounds", "Unlaunch", skin)

    @skins.command(name="dsi", aliases=["dsimenu"])
    async def skin_dsimenu(self, ctx, *args):
        """Links to the DSi Menu skins page.\n
        To show a random skin: `skins dsi [-r]`
        To search for a background: `s`kins dsi [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "DSi Menu Skins", "Nintendo DSi", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "DSi Menu Skins", "Nintendo DSi", skin)

    @skins.command(name="3ds", aliases=["3dsmenu"])
    async def skin_3dsmenu(self, ctx, *args):
        """Links to the 3DS Menu skins page.\n
        To show a random skin: `skins 3ds [-r]`
        To search for a background: `skins 3ds [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "3DS Menu Skins", "Nintendo 3DS", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "3DS Menu Skins", "Nintendo 3DS", skin)

    @skins.command(name="r4", aliases=["r4theme"])
    async def skin_r4menu(self, ctx, *args):
        """Links to the R4 Original Menu skins page.\n
        To show a random skin: `skins r4 [-r]`
        To search for a background: `skins r4 [search parameter]`"""
        if args and args[0] == "-r":
            await self.skinparse(ctx, "R4 Original Menu Skins", "R4 Original", israndom=True)
        else:
            skin = "".join(args)
            await self.skinparse(ctx, "R4 Original Menu Skins", "R4 Original", skin)


def setup(bot):
    bot.add_cog(UniStore(bot))

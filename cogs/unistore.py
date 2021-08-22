import discord
import requests
import re
import math
import random

from discord.ext import commands
from utils.utils import web_name


class UniStore(commands.Cog):
    """Commands related to UniStore searching"""

    def __init__(self, bot):
        self.bot = bot

    def searchdb(self, query, id):
        # regex escape
        query = re.sub(r"([-\/\\^$*+?.()|[\]{}])", r"\\\1", query)
        # make fuzzy
        query = re.sub(r"(\\?.)", r"\1.*", query)  # put .* between everything
        query = re.sub(r"\\-|_| ", r"[-_ ]", query)  # make - _ and space the same
        # try match
        return len(re.findall(query, id["title"], flags=re.IGNORECASE)) > 0

    def udbembed(self, embed, appid):
        embed.title = appid["title"]
        embed.color = int(appid['color'][1:], 16)
        embed.set_author(name=appid["author"], icon_url=appid["avatar"] if "avatar" in appid else discord.Embed.Empty)
        embed.set_thumbnail(url=appid["icon"] if "icon" in appid else (appid["image"] if "image" in appid else (appid["avatar"] if "avatar" in appid else discord.Embed.Empty)))
        embed.description = appid["description"]
        embed.url += appid["systems"][0].lower() + "/" + web_name(appid["title"])
        return embed

    async def udbparse(self, ctx, app="", israndom=0):
        unistore = None
        if israndom == 1 and app != "":
            unistore = requests.get("https://raw.githubusercontent.com/Universal-Team/db/master/docs/data/full.json").json()
        embed = discord.Embed(title="Universal-DB")
        embed.set_author(name="Universal-Team")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/49733679?s=400&v=4")
        embed.description = "A database of DS and 3DS homebrew"
        embed.url = "https://db.universal-team.net/"
        if israndom == 1:
            await ctx.send(embed=self.udbembed(embed, unistore[math.floor(random.random() * len(unistore))]))
            return
        if app != "":
            for appid in unistore:
                if self.searchdb(app, appid):
                    await ctx.send(embed=self.udbembed(embed, appid))
                    return
            await ctx.send("App cannot be found. Please try again.")
            return
        await ctx.send(embed=embed)

    def skinembed(self, embed, skinid):
        embed.set_author(name=skinid["author"], icon_url=skinid["avatar"] if "avatar" in skinid else discord.Embed.Empty)
        embed.set_thumbnail(url=skinid["icon"])
        embed.title = skinid["title"]
        embed.description = skinid["description"]
        embed.url += web_name(skinid["title"])
        return embed

    async def skinparse(self, ctx, title, extension, skin=""):
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
        if skin != "":
            unistore = requests.get("https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/docs/data/full.json").json()
            for skinid in unistore:
                if self.searchdb(skin, skinid) and skinid["console"] == extension:
                    await ctx.send(embed=self.skinembed(embed, skinid))
                    return
            await ctx.send("Skin cannot be found. Please try again.")
            return
        await ctx.send(embed=embed)

    @commands.command(aliases=["universaldb"])
    async def udb(self, ctx, *args):
        """Links to Universal-DB and/or one of the apps\n
        Usage: """
        if args and args[0] == "-r":
            await self.udbparse(ctx, israndom=1)
        else:
            app = "".join(args)
            await self.udbparse(ctx, app)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def skins(self, ctx):
        """Links to a database of TWiLight Menu++ skins and Unlaunch backgrounds"""
        embed = discord.Embed(title="Skins")
        embed.set_author(name="DS-Homebrew")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.description = "A collection of skins for TWiLight Menu++ from DS-Homebrew/twlmenu-extras on GitHub"
        embed.url = "https://skins.ds-homebrew.com/"
        await ctx.send(embed=embed)

    @skins.command(name="unlaunch")
    async def skin_unlaunch(self, ctx, *args):
        """Links to the Unlaunch skins page"""
        skin = "".join(args)
        await self.skinparse(ctx, "Unlaunch Backgrounds", "Unlaunch", skin)

    @skins.command(name="dsi", aliases=["dsimenu"])
    async def skin_dsimenu(self, ctx, *args):
        skin = "".join(args)
        await self.skinparse(ctx, "DSi Menu Skins", "Nintendo DSi", skin)

    @skins.command(name="3ds", aliases=["3dsmenu"])
    async def skin_3dsmenu(self, ctx, *args):
        skin = "".join(args)
        await self.skinparse(ctx, "3DS Menu Skins", "Nintendo 3DS", skin)

    @skins.command(name="r4", aliases=["r4theme"])
    async def skin_r4menu(self, ctx, *args):
        skin = "".join(args)
        await self.skinparse(ctx, "R4 Original Menu Skins", "R4 Original", skin)


def setup(bot):
    bot.add_cog(UniStore(bot))

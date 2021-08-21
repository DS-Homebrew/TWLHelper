import discord
import requests
import re

from discord.ext import commands
from utils.utils import web_name


class UniStore(commands.Cog):
    """Commands related to UniStore searching"""

    def __init__(self, bot):
        self.bot = bot

    async def udb_embed(self, ctx, title, app=""):
        unistore = requests.get("https://raw.githubusercontent.com/Universal-Team/db/master/docs/unistore/universal-db.unistore").json()
        embed = discord.Embed(title=title)
        embed.set_author(name="Universal-Team")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/49733679?s=400&v=4")
        embed.description = "A database of DS and 3DS homebrew"
        embed.url = "https://db.universal-team.net/"
        if app != "":
            for appid in unistore["storeContent"]:
                if appid["info"]["title"].lower().find(app.lower()) != -1:
                    embed.set_author(name=appid["info"]["author"])
                    # embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/" + iconname + ".png")
                    embed.title = appid["info"]["title"]
                    embed.description = appid["info"]["description"]
                    embed.url += appid["info"]["console"][0] + web_name(appid["info"]["title"])
                    await ctx.send(embed=embed)
                    return
            await ctx.send("App cannot be found. Please try again.")
            return
        await ctx.send(embed=embed)

    @commands.command(aliases=["universaldb"])
    async def udb(self, ctx, app=""):
        await self.udb_embed(ctx, "Universal-DB", app)


def setup(bot):
    bot.add_cog(UniStore(bot))

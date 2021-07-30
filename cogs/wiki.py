import discord

from discord.ext import commands
from inspect import cleandoc
from .results import faqs


class Wiki(commands.Cog):
    """
    Commands that link to wiki pages
    """

    def __init__(self, bot):
        self.bot = bot

    def check_arg(self, message, arg):
        message = message.lower()
        if message in arg:
            return True
        return False

    async def simple_embed(self, ctx, text, *, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = cleandoc(text)
        await ctx.send(embed=embed)

    def web_name(self, name):
        name = name.lower()
        out = ""
        for letter in name:
            if letter in "abcdefghijklmnopqrstuvwxyz0123456789-_.":
                out += letter
            elif letter == " ":
                out += "-"
        return out

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def faq(self, ctx):
        """Links to the FAQ for an application."""
        await ctx.send_help(ctx.command)

    @faq.command(aliases=["twl", "twlmenu", "twilightmenu"])
    async def twilight(self, ctx, *, arg=""):
        embed = discord.Embed(title="TWiLight Menu++ FAQ")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.twlmenu:
                if arg.lower() in faq.lower():
                    embed.url += "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)

    @faq.command(aliases=["nds-bootstrap", "bootstrap", "ndsbs", "bs"])
    async def ndsbootstrap(self, ctx, *, arg=""):
        embed = discord.Embed(title="nds-bootstrap FAQ")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/nds-bootstrap/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.bootstrap:
                if arg.lower() in faq.lower():
                    embed.url += "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)

    @faq.command(aliases=["gbar2"])
    async def gbarunner2(self, ctx, *, arg=""):
        embed = discord.Embed(title="GBARunner2 FAQ")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/gbarunner2/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.gbar2:
                if arg.lower() in faq.lower():
                    embed.url += "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)

    @faq.command(aliases=["hiya"])
    async def hiyacfw(self, ctx):
        embed = discord.Embed(title="hiyaCFW Troubleshooting")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/hiyacfw/troubleshooting.html"
        embed.description = "Troubleshooting"
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        """Links and/or information on updating apps or system."""
        await ctx.send_help(ctx.command)

    @update.command(aliases=["twlmenu", "twl", "twilight"])
    async def twilightmenu(self, ctx, *, arg=""):
        embed = discord.Embed(title="TWiLight Menu++ Update Guide")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/updating"
        embed.description = "How to update TWiLight Menu++"
        if arg != "":
            if self.check_arg(arg, ("3ds",)):
                embed.url += "-3ds"
                embed.description += " on the 3DS"
            elif self.check_arg(arg, ("dsi",)):
                embed.url += "-dsi"
                embed.description += " on the DSi"
            elif self.check_arg(arg, ("flashcard", "flashcart", "ds")):
                embed.url += "-flashcard"
                embed.description += " on flashcards"
        embed.url += ".html"
        await ctx.send(embed=embed)

    @commands.command()
    async def widescreen(self, ctx):
        """Widescreen for 3DS TWLMenu++"""
        embed = discord.Embed(title="Playing in Widescreen")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/playing-in-widescreen.html"
        embed.description = "Playing in widescreen with TWiLight Menu++ on 3DS"
        await ctx.send(embed=embed)

    @commands.command(aliases=["forwarders", "forwarder", "twlforwarders"])
    async def ndsforwarders(self, ctx):
        """Links to nds forwarders"""
        embed = discord.Embed(title="NDS Forwarder Guide")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.url = "https://wiki.ds-homebrew.com/ds-index/forwarders.html"
        embed.description = "Creating forwarders for nds-bootstrap"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))

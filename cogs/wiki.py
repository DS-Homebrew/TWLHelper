import discord
import sys

from discord.ext import commands
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

    @commands.group(cooldown=commands.Cooldown(0, 0, commands.BucketType.channel), invoke_without_command=True, case_insensitive=True)
    async def faq(self, ctx):
        """Links to the FAQ for an application."""
        await ctx.send_help(ctx.command)

    @faq.command(aliases=["twl", "twlmenu"], cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def twilight(self, ctx, *, arg=""):
        embed = discord.Embed(title="TWiLight Menu++ FAQ")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.twlmenu:
                if arg.lower() in faq.lower():
                    embed.url = embed.url + "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)
    
    @faq.command(aliases=["nds-bootstrap", "bootstrap", "ndsbs", "bs"], cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def ndsbootstrap(self, ctx, *, arg=""):
        embed = discord.Embed(title="nds-bootstrap FAQ")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/nds-bootstrap/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.bootstrap:
                if arg.lower() in faq.lower():
                    embed.url = embed.url + "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)

    @faq.command(aliases=["gbar2"], cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def gbarunner2(self, ctx, *, arg=""):
        embed = discord.Embed(title="GBARunner2 FAQ")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/gbarunner2/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.gbar2:
                if arg.lower() in faq.lower():
                    embed.url = embed.url + "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)

    @faq.command(aliases=["hiya"], cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def hiyacfw(self, ctx):
        embed = discord.Embed(title="hiyaCFW Troubleshooting")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/hiyacfw/troubleshooting.html"
        embed.description = "Troubleshooting"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))

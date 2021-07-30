import discord

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

    def embed(self, title):
        embed = discord.Embed(title=title)
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.url = "https://wiki.ds-homebrew.com/"
        return embed

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

    @faq.command(name="twilight", aliases=["twl", "twlmenu", "twilightmenu"])
    async def twilight_faq(self, ctx, *, arg=""):
        embed = self.embed("TWiLight Menu++ FAQ")
        embed.title = "TWiLight Menu++ FAQ"
        embed.url += "twilightmenu/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.twlmenu:
                if arg.lower() in faq.lower():
                    embed.url += "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)

    @faq.command(aliases=["nds-bootstrap", "bootstrap", "ndsbs", "bs"])
    async def ndsbootstrap(self, ctx, *, arg=""):
        embed = self.embed("nds-bootstrap FAQ")
        embed.url += "nds-bootstrap/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.bootstrap:
                if arg.lower() in faq.lower():
                    embed.url += "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)

    @faq.command(aliases=["gbar2"])
    async def gbarunner2(self, ctx, *, arg=""):
        embed = self.embed("GBARunner2 FAQ")
        embed.url += "gbarunner2/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            for faq in faqs.gbar2:
                if arg.lower() in faq.lower():
                    embed.url += "?faq=" + self.web_name(faq)
                    embed.description = faq
        await ctx.send(embed=embed)

    @faq.command(aliases=["hiya"])
    async def hiyacfw(self, ctx):
        embed = self.embed("hiyaCFW Troubleshooting")
        embed.url += "hiyacfw/troubleshooting.html"
        embed.description = "Troubleshooting"
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        """Links and/or information on updating apps or system."""
        await ctx.send_help(ctx.command)

    @update.command(name="twilight", aliases=["twlmenu", "twl", "twilightmenu"])
    async def twilight_update(self, ctx, *, arg=""):
        embed = self.embed("TWiLight Menu++ Update Guide")
        embed.url += "twilightmenu/updating"
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

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def install(self, ctx):
        """Links and/or information on installing apps."""
        await ctx.send_help(ctx.command)

    @install.command(name="twilight", aliases=["twlmenu", "twl", "twilightmenu"])
    async def twilight_install(self, ctx, *, arg=""):
        embed = self.embed("TWiLight Menu++ Installation Guide")
        embed.url += "twilightmenu/installing"
        embed.description = "How to install TWiLight Menu++"
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

    @install.command(name="hiyacfw", aliases=["hiya"])
    async def hiyacfw_install(self, ctx, *, arg=""):
        embed = self.embed("hiyaCFW Installation Guide")
        embed.url += "hiyacfw/installing"
        embed.description = "How to install hiyaCFW on the DSi"
        await ctx.send(embed=embed)

    @commands.command(aliases=["ds-index"])
    async def dsindex(self, ctx):
        """Links to the DS index"""
        embed = self.embed("Nintendo DS Modding Index")
        embed.url += "ds-index/"
        embed.description = "An explanation of all things DS modding"
        await ctx.send(embed=embed)

    @commands.command()
    async def widescreen(self, ctx):
        """Widescreen for 3DS TWLMenu++"""
        embed = self.embed("Playing in Widescreen")
        embed.url += "twilightmenu/playing-in-widescreen.html"
        embed.description = "Playing in widescreen with TWiLight Menu++ on 3DS"
        await ctx.send(embed=embed)

    @commands.command(aliases=["forwarders", "forwarder", "twlforwarders"])
    async def ndsforwarders(self, ctx):
        """Links to nds forwarders"""
        embed = self.embed("NDS Forwarder Guide")
        embed.url += "ds-index/forwarders.html"
        embed.description = "Creating forwarders for nds-bootstrap"
        await ctx.send(embed=embed)

    @commands.command()
    async def hardmod(self, ctx):
        """Links to the DSi hardmod guide"""
        embed = self.embed("Nintendo DSi Hardmod Guide")
        embed.url += "ds-index/hardmod.html"
        embed.description = "How to hardmod a Nintendo DSi"
        await ctx.send(embed=embed)

    @commands.command(aliases=["serverrules", "discordrules"])
    async def rules(self, ctx):
        """Links to the DSi hardmod guide"""
        embed = self.embed("DS⁽ⁱ⁾ Mode Hacking Rules")
        embed.url += "community/discord-rules.html"
        embed.description = "The rules for the DS⁽ⁱ⁾ Mode Hacking Discord server"
        await ctx.send(embed=embed)

    @commands.command(aliases=["discordinfo"])
    async def serverinfo(self, ctx):
        """Links to the DSi hardmod guide"""
        embed = self.embed("DS⁽ⁱ⁾ Mode Hacking Info")
        embed.url += "community/discord-info.html"
        embed.description = "Information for the DS⁽ⁱ⁾ Mode Hacking Discord server"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))

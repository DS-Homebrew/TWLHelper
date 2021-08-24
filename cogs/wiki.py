import discord
import requests
import re

from discord.ext import commands
from utils.utils import check_arg, web_name


class Wiki(commands.Cog):
    """
    Commands that link to wiki pages
    """

    def __init__(self, bot):
        self.bot = bot

    def git_name(self, name):
        name = name.lower()
        url = "https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/" + name + "/faq.md"
        return url

    def read_to_next(self, file, iter):
        line = file[iter]
        out = ""
        while "#### " not in line or "#####" in line:
            out += '\n' + file[iter]
            iter += 1
            if iter < len(file):
                line = file[iter]
            else:
                break
        return re.sub("##### (.*)", "**\\1**", out)

    def embed(self, title):
        embed = discord.Embed(title=title)
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.url = "https://wiki.ds-homebrew.com/"
        return embed

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def faq(self, ctx):
        """Links to the FAQ for an application"""
        await ctx.send_help(ctx.command)

    @faq.command(name="twilight", aliases=["twl", "twlmenu", "twilightmenu"])
    async def twilight_faq(self, ctx, *, arg=""):
        embed = self.embed("TWiLight Menu++ FAQ")
        embed.title = "TWiLight Menu++ FAQ"
        embed.url += "twilightmenu/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            page = requests.get(self.git_name("twilightmenu")).text
            faqpage = page.splitlines()
            iter = 0
            for faq in faqpage:
                iter += 1
                if arg.lower() in faq.lower() and "#### " in faq.lower():
                    title = faq[5:]
                    embed.url += "?faq=" + web_name(title)
                    embed.description = "**" + title + "**" + "\n" + self.read_to_next(faqpage, iter)
        await ctx.send(embed=embed)

    @faq.command(aliases=["nds-bootstrap", "bootstrap", "ndsbs", "bs"])
    async def ndsbootstrap(self, ctx, *, arg=""):
        embed = self.embed("nds-bootstrap FAQ")
        embed.url += "nds-bootstrap/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            page = requests.get(self.git_name("nds-bootstrap")).text
            faqpage = page.splitlines()
            iter = 0
            for faq in faqpage:
                iter += 1
                if arg.lower() in faq.lower() and "#### " in faq.lower():
                    title = faq[5:]
                    embed.url += "?faq=" + web_name(title)
                    embed.description = "**" + title + "**" + "\n" + self.read_to_next(faqpage, iter)
        await ctx.send(embed=embed)

    @faq.command(aliases=["gbar2"])
    async def gbarunner2(self, ctx, *, arg=""):
        embed = self.embed("GBARunner2 FAQ")
        embed.url += "gbarunner2/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            page = requests.get(self.git_name("gbarunner2")).text
            faqpage = page.splitlines()
            iter = 0
            for faq in faqpage:
                iter += 1
                if arg.lower() in faq.lower() and "#### " in faq.lower():
                    title = faq[5:]
                    embed.url += "?faq=" + web_name(title)
                    embed.description = "**" + title + "**" + "\n" + self.read_to_next(faqpage, iter)
        await ctx.send(embed=embed)

    @faq.command(aliases=["hiya"])
    async def hiyacfw(self, ctx, *, arg=""):
        embed = self.embed("hiyaCFW FAQ")
        embed.url += "hiyacfw/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg != "":
            page = requests.get(self.git_name("hiyacfw")).text
            faqpage = page.splitlines()
            iter = 0
            for faq in faqpage:
                iter += 1
                if arg.lower() in faq.lower() and "#### " in faq.lower():
                    title = faq[5:]
                    embed.url += "?faq=" + web_name(title)
                    embed.description = "**" + title + "**" + "\n" + self.read_to_next(faqpage, iter)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        """Links and/or information on updating apps or system"""
        await ctx.send_help(ctx.command)

    @update.command(name="twilight", aliases=["twlmenu", "twl", "twilightmenu"])
    async def twilight_update(self, ctx, *, arg=""):
        embed = self.embed("TWiLight Menu++ Update Guide")
        embed.url += "twilightmenu/updating"
        embed.description = "How to update TWiLight Menu++"
        if arg != "":
            if check_arg(arg, ("3ds",)):
                embed.url += "-3ds"
                embed.description += " on the 3DS"
            elif check_arg(arg, ("dsi",)):
                embed.url += "-dsi"
                embed.description += " on the DSi"
            elif check_arg(arg, ("flashcard", "flashcart", "ds")):
                embed.url += "-flashcard"
                embed.description += " on flashcards"
        embed.url += ".html"
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def install(self, ctx):
        """Links and/or information on installing apps"""
        await ctx.send_help(ctx.command)

    @install.command(name="twilight", aliases=["twlmenu", "twl", "twilightmenu"])
    async def twilight_install(self, ctx, *, arg=""):
        embed = self.embed("TWiLight Menu++ Installation Guide")
        embed.url += "twilightmenu/installing"
        embed.description = "How to install TWiLight Menu++"
        if arg != "":
            if check_arg(arg, ("3ds",)):
                embed.url += "-3ds"
                embed.description += " on the 3DS"
            elif check_arg(arg, ("dsi",)):
                embed.url += "-dsi"
                embed.description += " on the DSi"
            elif check_arg(arg, ("flashcard", "flashcart", "ds")):
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

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def uninstall(self, ctx):
        """Links and/or information on uninstalling apps"""
        await ctx.send_help(ctx.command)

    @uninstall.command(name="twilight", aliases=["twlmenu", "twl", "twilightmenu"])
    async def twilight_uninstall(self, ctx, *, arg=""):
        systems = ("3ds", "dsi", "ds")
        embed = self.embed("TWiLight Menu++ Uninstall Guide")
        embed.url += "twilightmenu/uninstalling"
        embed.description = "How to uninstall TWiLight Menu++"
        if arg != "":
            if check_arg(arg, ("3ds",)):
                embed.url += "-3ds"
                embed.description += " on the 3DS"
            elif check_arg(arg, ("dsi", "flashcard", "flashcart", "ds")):
                embed.url += "-ds"
                embed.description += " on the DSi and/or flashcards"
        else:
            await ctx.send(f"Please specify a console. Valid options are: {', '.join([x for x in systems])}.")
            return
        embed.url += ".html"
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
        """Links to the nds-bootstrap forwarder guide"""
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

    @commands.command(aliases=["wi-fi"])
    async def wifi(self, ctx):
        """Links to the Wi-Fi tutorial"""
        embed = self.embed("Connecting DS Games to the Internet")
        embed.url += "ds-index/wifi.html"
        embed.description = "Connecting your DS⁽ⁱ⁾ to the Internet to play online"
        await ctx.send(embed=embed)

    @commands.command()
    async def emulators(self, ctx):
        """Links to the emulator index page"""
        embed = self.embed("Emulators on the DS")
        embed.url += "ds-index/emulators.html"
        embed.description = "A reference on Emulators on the DS"
        await ctx.send(embed=embed)

    @commands.command()
    async def retail(self, ctx):
        """Links to the list of retail DS games"""
        embed = self.embed("Retail ROMs")
        embed.url += "ds-index/retail-roms.html"
        embed.description = "A reference on retail DS games"
        await ctx.send(embed=embed)

    @commands.command(aliases=["special", "specgames"])
    async def specialgames(self, ctx):
        """Links to the list of special games"""
        embed = self.embed("Special Games")
        embed.url += "ds-index/special-games.html"
        embed.description = "A list of DS games with special features"
        await ctx.send(embed=embed)

    @commands.command()
    async def unlaunchbg(self, ctx):
        """Links to a guide to changing Unlaunch background"""
        embed = self.embed("Custom Unlaunch Backgrounds")
        embed.url += "twilightmenu/custom-unlaunch-backgrounds.html"
        embed.description = "How to make custom Unlaunch backgrounds and install them using TWiLight Menu++"
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def bios(self, ctx):
        await ctx.send_help(ctx.command)

    @bios.command()
    async def gba(self, ctx, arg=""):
        embed = self.embed("GBA BIOS Info")
        embed.url += "gbarunner2/bios.html"
        embed.description = "Information on the GBA BIOS and how to dump it"
        if arg == "nds" or arg == "gba" or arg == "flashcard" or arg == "flashcart":
            embed.title = "Dumping GBA BIOS from a DS"
            embed.description = "Also dump from a GBA"
            embed.url = "https://glazedbelmont.github.io/gbabiosdump/#gameboy-advance-sp-micro-ds-ds-lite.html"
            embed.set_author(name="GlaZed Belmont")
            embed.set_thumbnail(url="https://raw.githubusercontent.com/GlaZedBelmont/GlaZedBelmont.github.io/master/img/glazed.png")
        elif arg == "3ds":
            embed.title = "Dumping GBA BIOS from a 3DS"
            embed.description = "Tutorial to dump a GBA BIOS from a 3DS VC title"
            embed.url = "https://glazedbelmont.github.io/gbabiosdump/#virtual-console-title-from-a-3ds.html"
            embed.set_author(name="GlaZed Belmont")
            embed.set_thumbnail(url="https://raw.githubusercontent.com/GlaZedBelmont/GlaZedBelmont.github.io/master/img/glazed.png")
        elif arg == "wii" or arg == "linkcable":
            embed.title = "Dumping GBA BIOS from a Wii"
            embed.description = "How to dump a GBA BIOS from a Wii or GameCube"
            embed.url = "https://github.com/FIX94/gba-link-cable-dumper"
            embed.set_author(name="FIX94")
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/12349638?v=4")
        await ctx.send(embed=embed)

    @bios.command()
    async def nds(self, ctx):
        embed = discord.Embed(title="Dumping NDS BIOS")
        embed.set_author(name="Arisotura")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/1311867?v=4")
        embed.url = "http://melonds.kuribo64.net/faq.php"
        embed.description = "How to dump the NDS BIOS from a DS, DSi or 3DS"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))

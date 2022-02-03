#
# ISC License

# Copyright (C) 2021-present DS-Homebrew

# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import discord
import re

from discord.ext import commands
from typing import Optional
from utils import check_arg, web_name, twilightmenu_alias, ndsbootstrap_alias


class Wiki(commands.Cog):
    """
    Commands that link to wiki pages
    """

    def __init__(self, bot):
        self.bot = bot

    async def read_faq(self, ctx, console, arg, embed):
        page = None
        r = await self.bot.session.get("https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/" + console.lower() + "/faq.md")
        if r.status == 200:
            page = await r.text()
        else:
            return await ctx.send(embed=embed)
        faqpage = page.splitlines()
        iter = 0
        field_title = None
        for faq in faqpage:
            iter += 1
            if arg.lower() in faq.lower() and "#### " in faq.lower():
                field_title = faq[5:]
                embed.url += "?faq=" + web_name(field_title)
                embed.description = discord.Embed.Empty
                break
        if embed.description != discord.Embed.Empty:
            return await ctx.send(embed=embed)
        line = faqpage[iter]
        field_description = ""
        while "#### " not in line or "#####" in line:
            field_description += '\n' + faqpage[iter]
            iter += 1
            if iter < len(faqpage):
                line = faqpage[iter]
            else:
                break
        field_description = re.sub("##### (.*)", "**\\1**", field_description)  # Change h5 to bold
        field_description = re.sub("<kbd(?: class=\"[^\"]*\")?>(.*?)</kbd>", "`\\1`", field_description)  # Change kbd to inline code
        field_description = re.sub("<.*?>(.*?)</.*?>", "\\1", field_description)  # Remove other HTML
        field_description = re.sub("<(area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr).*?>", "[\\1]", field_description)  # Remove self-closing HTML
        embed.add_field(name=field_title, value=field_description)
        await ctx.send(embed=embed)

    def read_glossary(self, file, iter):
        line = file[iter]
        out = ""
        while "### " not in line or "####" in line:
            out += '\n' + file[iter]
            iter += 1
            if iter < len(file):
                line = file[iter]
            else:
                break
        out = re.sub("#### (.*)", "**\\1**", out)  # Change h4 to bold
        out = re.sub("<kbd(?: class=\"[^\"]*\")?>(.*?)</kbd>", "`\\1`", out)  # Change kbd to inline code
        out = re.sub("<(.*?)>(.*?)<\\/\\1>", "\\2", out)  # Remove other HTML
        out = re.sub("<(area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr).*?>", "[\\1]", out)  # Remove self-closing HTML
        return out

    def read_rule(self, ctx, file, iter):
        line = file[iter]
        out = ""
        iter += 1
        while ("### " not in line and "## " not in line) or "####" in line:
            out += '\n' + file[iter]
            iter += 1
            if iter < len(file):
                line = file[iter]
            else:
                break
        out = re.sub("#### (.*)", "**\\1**", out)
        out = re.sub(r"\[#.+?\]\(.+?\\/(\d+)\)", "<#\\1>", out)
        return out

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

    @faq.command(name="twilight", aliases=twilightmenu_alias)
    async def twilight_faq(self, ctx, *, arg=""):
        """TWiLight Menu Frequently Asked Questions.
        Usage: faq twilight [search parameter]"""
        embed = self.embed("TWiLight Menu++ FAQ")
        embed.url += "twilightmenu/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg == "":
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "twilightmenu", arg, embed)

    @faq.command(aliases=ndsbootstrap_alias)
    async def ndsbootstrap(self, ctx, *, arg=""):
        """nds-bootstrap Frequently Asked Questions.
        Usage: faq ndsbootstrap [search parameter]"""
        embed = self.embed("nds-bootstrap FAQ")
        embed.url += "nds-bootstrap/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg == "":
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "nds-bootstrap", arg, embed)

    @faq.command(aliases=["gbar2"])
    async def gbarunner2(self, ctx, *, arg=""):
        """GBARunner2 Frequently Asked Questions.
        Usage: faq gbarunner2 [search parameter]"""
        embed = self.embed("GBARunner2 FAQ")
        embed.url += "gbarunner2/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg == "":
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "gbarunner2", arg, embed)

    @faq.command(aliases=["gm9i"])
    async def godmode9i(self, ctx, *, arg=""):
        """GodMode9i Frequently Asked Questions.
        Usage: faq godmode9i [search parameter]"""
        embed = self.embed("GodMode9i FAQ")
        embed.url += "godmode9i/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if arg == "":
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "godmode9i", arg, embed)

    @faq.command(aliases=["hiya"])
    async def hiyacfw(self, ctx):
        """hiyaCFW Frequently Asked Questions.
        This does not have a FAQ search function."""
        embed = self.embed("hiyaCFW FAQ")
        embed.url += "hiyacfw/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        """Links and/or information on updating apps or system"""
        await ctx.send_help(ctx.command)

    @update.command(name="twilight", aliases=twilightmenu_alias)
    async def twilight_update(self, ctx, *, arg=""):
        """TWiLight Menu update guide.
        Usage: update twilight [3ds, dsi, ds]"""
        embed = self.embed("TWiLight Menu++ Update Guide")
        embed.url += "twilightmenu/updating"
        embed.description = "How to update TWiLight Menu++"
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

    @commands.command()
    async def glossary(self, ctx, *, arg=""):
        """nds-bootstrap Glossary"""
        embed = self.embed("nds-bootstrap Glossary")
        embed.url += "nds-bootstrap/glossary.html"
        embed.description = "Glossary for nds-bootstrap"
        page = None
        r = None
        if arg != "":
            r = await self.bot.session.get("https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/nds-bootstrap/glossary.md")
            if r.status == 200:
                page = await r.text()
            else:
                return await ctx.send(embed=embed)
            glossary = page.splitlines()
            iter = 0
            for item in glossary:
                iter += 1
                if arg.lower() in item.lower() and "### " in item.lower():
                    title = item[4:]
                    embed.url += "#" + web_name(title)
                    embed.description = discord.Embed.Empty
                    embed.add_field(name=title, value=self.read_glossary(glossary, iter))
                    break
            await ctx.send(embed=embed)

    @commands.command(aliases=["serverrules", "discordrules"])
    async def rule(self, ctx, num: Optional[int]):
        """Links to the server rules"""
        embed = self.embed("DS⁽ⁱ⁾ Mode Hacking Rules")
        embed.url += "community/discord-rules.html"
        embed.description = "The rules for the DS⁽ⁱ⁾ Mode Hacking Discord server"
        if not num:
            await ctx.send(embed=embed)
        else:
            if num < 0 or num > 12:
                return await ctx.send("Invalid rule number. Please try again.")
            page = None
            r = await self.bot.session.get("https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/community/discord-rules.md")
            if r.status == 200:
                page = await r.text()
            numstr = str(num)
            rulepage = page.splitlines()
            message = ""
            iter = 0
            rulenum = "### " + numstr
            for rule in rulepage:
                iter += 1
                if rulenum in rule.lower():
                    message = "**Rule " + rule[4:] + "**\n"
                    message += self.read_rule(ctx, rulepage, iter)
                    break
            await ctx.send(message)

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

    @commands.command(aliases=['sfx'])
    async def twlsfx(self, ctx):
        """Links to a guide to custom TWiLight Menu SFX"""
        embed = self.embed("DSi/3DS Skins - Custom SFX")
        embed.url += "twilightmenu/custom-dsi-3ds-sfx.html"
        embed.description = "How to use custom background music and sound effects in DSi and 3DS skins for TWiLight Menu++"
        await ctx.send(embed=embed)

    @commands.command()
    async def boxartguide(self, ctx):
        """Links to a guide to get Box Art"""
        embed = self.embed("How to Get Box Art")
        embed.url += "twilightmenu/how-to-get-box-art.html"
        embed.description = "How to add box art to TWiLight Menu++"
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def bios(self, ctx):
        """BIOS info page"""
        await ctx.send_help(ctx.command)

    @bios.command()
    async def gba(self, ctx, arg=""):
        """GBA BIOS Info/dump page.
        Usage: bios gba [nds, gba, 3ds, wii]"""
        embed = self.embed("GBA BIOS Info")
        embed.url += "gbarunner2/bios.html"
        embed.description = "Information on the GBA BIOS and how to dump it"
        if check_arg(arg, ("nds", "gba", "flashcard", "flashcart")):
            embed.title = "Dumping GBA BIOS from a DS"
            embed.description = "Also dump from a GBA"
            embed.url = "https://glazedbelmont.github.io/gbabiosdump/#gameboy-advance-sp-micro-ds-ds-lite.html"
            embed.set_author(name="GlaZed Belmont")
            embed.set_thumbnail(url="https://raw.githubusercontent.com/GlaZedBelmont/GlaZedBelmont.github.io/master/img/glazed.png")
        elif check_arg(arg, ("3ds",)):
            embed.title = "Dumping GBA BIOS from a 3DS"
            embed.description = "Tutorial to dump a GBA BIOS using open_agb_firm"
            embed.url = "https://glazedbelmont.github.io/gbabiosdump/#virtual-console-title-from-a-3ds.html"
            embed.set_author(name="GlaZed Belmont")
            embed.set_thumbnail(url="https://raw.githubusercontent.com/GlaZedBelmont/GlaZedBelmont.github.io/master/img/glazed.png")
        elif check_arg(arg, ("wii", "linkcable")):
            embed.title = "Dumping GBA BIOS from a Wii"
            embed.description = "How to dump a GBA BIOS from a Wii or GameCube"
            embed.url = "https://github.com/FIX94/gba-link-cable-dumper"
            embed.set_author(name="FIX94")
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/12349638?v=4")
        await ctx.send(embed=embed)

    @bios.command(aliases=["ds", "dsi"])
    async def nds(self, ctx):
        """NDS BIOS Dumping"""
        embed = discord.Embed(title="Dumping NDS BIOS")
        embed.set_author(name="Arisotura")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/1311867?v=4")
        embed.url = "http://melonds.kuribo64.net/faq.php"
        embed.description = "How to dump the NDS BIOS from a DS, DSi or 3DS"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))

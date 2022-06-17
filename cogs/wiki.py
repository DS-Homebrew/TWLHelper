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
import re

from discord.ext import commands
from typing import Optional
from utils import check_arg, twilightmenu_alias


class Wiki(commands.Cog):
    """
    Commands that link to wiki pages
    """

    def __init__(self, bot):
        self.bot = bot

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
        """Displays an embed with a link telling you how to play in widescreen"""
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
    async def rule(self, ctx: commands.Context, num: Optional[int]):
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
            await ctx.send(message, suppress_embeds=True)

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
        embed.description = "A reference on emulators & loaders on the DS"
        await ctx.send(embed=embed)

    @commands.command()
    async def retail(self, ctx):
        """Links to the reference page for miscellaneous information on DS games"""
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
    async def customskins(self, ctx):
        """Displays an embed with a link to a guide on custom TWiLight Menu++ skins"""
        embed = self.embed("Custom DSi/3DS Skins")
        embed.url += "twilightmenu/custom-dsi-3ds-skins.html"
        embed.description = "How to Create DSi/3DS Skins for TWiLight Menu++"
        await ctx.send(embed=embed)

    @commands.command(aliases=["ramdisks"])
    async def ramdisk(self, ctx):
        """Links to the RAM Disk creation tutorial"""
        embed = self.embed("Creating RAM Disks")
        embed.url += "twilightmenu/creating-ram-disks.html"
        embed.description = "How to create RAM Disks for using older homebrew with nds-bootstrap"
        await ctx.send(embed=embed)

    @commands.command(aliases=["icons", "banner", "banners", "customicon", "customicons", "custombanner", "custombanners"])
    async def icon(self, ctx):
        """Links to the custom icons and banners page"""
        embed = self.embed("How to Get custom Icons and Banners")
        embed.url += "twilightmenu/how-to-get-custom-icons.html"
        embed.description = "How to get custom icons and banners for TWiLight Menu++"
        await ctx.send(embed=embed)

    @commands.command(aliases=["dlp", "downloadplay"])
    async def pictochat(self, ctx):
        """Links to the page for getting PictoChat and DS Download Play on the DS Classic Menu"""
        embed = self.embed("Download Play/PictoChat in the DS Classic Menu")
        embed.url += "twilightmenu/download-play-pictochat.html"
        embed.description = "How to get PictoChat and DS Download Play on the DS Classic Menu in TWiLight Menu++"
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


async def setup(bot):
    await bot.add_cog(Wiki(bot))

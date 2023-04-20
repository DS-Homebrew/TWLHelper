#
# Copyright (C) 2021-2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
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
    async def twilight_update(self, ctx):
        """TWiLight Menu update guide."""
        embed = self.embed("TWiLight Menu++ Update Guide")
        embed.url = None  # lol
        embed.description = "How to update TWiLight Menu++"
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="3DS", url="http://wiki.ds-homebrew.com/twilightmenu/updating-3ds.html"))
        view.add_item(discord.ui.Button(label="DSi", url="http://wiki.ds-homebrew.com/twilightmenu/updating-dsi.html"))
        view.add_item(discord.ui.Button(label="Flashcard", url="http://wiki.ds-homebrew.com/twilightmenu/updating-flashcard.html"))
        await ctx.send(embed=embed, view=view)

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
            page = None
            async with self.bot.session.get(f"https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/community/rules/{num}.md") as r:
                if r.status == 404:
                    return await ctx.send("Invalid rule number. Please try again.")
                elif r.status != 200:
                    return await ctx.send("Unable to fetch rules. Pleas try again later.")
                page = await r.text()
            page = re.sub("### (.*)", "**Rule \\1**", page)
            await ctx.send(page, suppress_embeds=True)

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
        if not arg:
            embed.url += "gbarunner2/bios.html"
            embed.description = "Information on the GBA BIOS and how to dump it"
        elif check_arg(arg, ("nds", "gba", "flashcard", "flashcart")):
            embed.title = "Dumping GBA BIOS from a DS or GBA"
            embed.description = "Tutorial to dump a GBA BIOS using a GBA flashcart"
            embed.url += "gbarunner2/bios-dump.html?tab=gba-flashcart"
        elif check_arg(arg, ("3ds",)):
            embed.title = "Dumping GBA BIOS from a 3DS"
            embed.description = "Tutorial to dump a GBA BIOS using open_agb_firm"
            embed.url += "gbarunner2/bios-dump.html?tab=gba-flashcart"
        elif check_arg(arg, ("wii", "linkcable")):
            embed.title = "Dumping GBA BIOS from a Wii"
            embed.description = "How to dump a GBA BIOS from a Wii or GameCube"
            embed.url = "https://github.com/FIX94/gba-link-cable-dumper"
            embed.set_author(name="FIX94")
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/12349638?v=4")
        await ctx.send(embed=embed)

    @bios.command(aliases=["ds", "dsi"])
    async def nds(self, ctx, arg=""):
        """NDS BIOS Dumping
        Usage: bios nds [nds, dsi, 3ds]"""
        embed = self.embed("Dumping NDS BIOS")
        embed.url += "ds-index/ds-bios-firmware-dump.html"
        if check_arg(arg, ("nds", "3ds", "flashcard", "flashcart")):
            embed.url += "?tab=flashcard"
            embed.description = "How to dump the NDS BIOS and firmware from a DS, DSi or 3DS using a flashcard"
        elif check_arg(arg, ("dsi",)):
            embed.url += "?tab=dsi-sd-card"
            embed.description = "How to dump the NDS and DSi BIOS and firmware from a DSi"
        else:
            embed.description = "How to dump the NDS and/or DSi BIOS and firmware"
        await ctx.send(embed=embed)

    @commands.command(aliases=['vp'])
    async def videoplayers(self, ctx: commands.Context):
        """Links to the video players page on the wiki"""
        embed = self.embed("Homebrew Video Players for the DS(i)")
        embed.url = "https://wiki.ds-homebrew.com/ds-index/videoplayers"
        embed.description = "How to play videos on the DS(i)"
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Wiki(bot))

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

from inspect import cleandoc
from discord.ext import commands

from utils import check_arg, Literal, twilightmenu_alias, ndsbootstrap_alias


class General(commands.Cog):
    """
    General commands
    """

    def __init__(self, bot):
        self.bot = bot

    async def simple_embed(self, ctx, text, *, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = cleandoc(text)
        await ctx.send(embed=embed)

    @commands.command(require_var_positional=True, usage="<3ds|wiiu|vwii|switch|wii|dsi|ngage>")
    async def guide(self, ctx, guide: Literal("3ds", "wiiu", "vwii", "switch", "wii", "dsi", "ngage")) -> None:  # noqa
        """Links to the recommended guides"""
        embed = discord.Embed(title="Guide")
        if check_arg(guide, '3ds'):
            embed.set_author(name="Nintendo Homebrew & Plailect")
            embed.set_thumbnail(url="https://nintendohomebrew.com/assets/img/nhplai.png")
            embed.url = "https://3ds.hacks.guide/"
            embed.description = "A complete guide to 3DS custom firmware, from stock to boot9strap"
            await ctx.send(embed=embed)
        elif check_arg(guide, ('wiiu',)):
            embed.set_author(name="Nintendo Homebrew")
            embed.set_thumbnail(url="https://i.imgur.com/CVSu1zc.png")
            embed.url = "https://wiiu.hacks.guide/"
            embed.description = "A guide to hacking the Nintendo Wii U"
            await ctx.send(embed=embed)
        elif check_arg(guide, ('vwii',)):
            embed.set_author(name="Nintendo Homebrew")
            embed.set_thumbnail(url="https://i.imgur.com/FclGzNz.png")
            embed.url = "https://wiiu.hacks.guide/#/vwii-modding"
            embed.description = "vWii modding guide"
            await ctx.send(embed=embed)
        elif check_arg(guide, ('switch')):
            embed.set_author(name="Nintendo Homebrew")
            embed.set_thumbnail(url="https://i.imgur.com/CVSu1zc.png")
            embed.url = "https://switchgui.de/switch-guide/"
            embed.description = "Switch CFW Guide"
            await ctx.send(embed=embed)
        elif check_arg(guide, 'wii'):
            embed.set_author(name="RiiConnect24")
            embed.set_thumbnail(url="https://i.imgur.com/KI6IXmm.png")
            embed.url = "https://wii.guide/"
            embed.description = "The complete guide to modding your Nintendo Wii"
            await ctx.send(embed=embed)
        elif check_arg(guide, 'dsi'):
            embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
            embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
            embed.url = "https://dsi.cfw.guide/"
            embed.description = "The complete guide to modding your Nintendo DSi"
            await ctx.send(embed=embed)
        elif check_arg(guide, 'ngage'):
            embed.set_author(name="N-Gage SDK")
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/98208101?s=200&v=4")
            embed.url = "https://hackaday.com/2022/01/27/an-up-to-date-development-environment-for-the-nokia-n-gage/"
            embed.description = "A homebrew development environment for the Nokia N-Gage"
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def install(self, ctx):
        """Links and/or information on installing apps"""
        await ctx.send_help(ctx.command)

    @install.command(name="twilight", aliases=twilightmenu_alias)
    async def twilight_install(self, ctx, *, arg=""):
        embed = discord.Embed(title="TWiLight Menu++ Installation Guide")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/installing"
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
    async def hiyacfw_install(self, ctx):
        embed = discord.Embed(title="hiyaCFW Installation Guide")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.url = "https://wiki.ds-homebrew.com/hiyacfw/installing.html"
        embed.description = "How to install hiyaCFW on the DSi"
        await ctx.send(embed=embed)

    @install.command(name="unlaunch")
    async def unlaunch_install(self, ctx):
        """Installing Unlaunch"""
        embed = discord.Embed(title="Installing Unlaunch")
        embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
        embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
        embed.url = "https://dsi.cfw.guide/installing-unlaunch.html"
        embed.description = "How to install Unlaunch on the DSi"
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def uninstall(self, ctx):
        """Links and/or information on uninstalling apps"""
        await ctx.send_help(ctx.command)

    @uninstall.command(name="twilight", aliases=twilightmenu_alias, usage="[3ds|dsi|ds]")
    async def twilight_uninstall(self, ctx, *, systems):
        """Displays an embed with a link that tells you how to uninstall TWiLight Menu++ for a certain system."""
        if not systems:
            systems = ("3ds", "dsi", "ds")
            await ctx.send(f'Please specify a console. Valid options are: {", ".join(list(systems))}.')

        embed = discord.Embed(title="TWiLight Menu++ Uninstall Guide")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/uninstalling"
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.description = "How to uninstall TWiLight Menu++"

        if check_arg(systems, ("3ds",)):
            embed.url += "-3ds"
            embed.description += " on the 3DS"
        elif check_arg(systems, ("dsi", "flashcard", "flashcart", "ds")):
            embed.url += "-ds"
            embed.description += " on the DSi and/or flashcards"

        embed.url += ".html"
        await ctx.send(embed=embed)

    @uninstall.command(name="unlaunch")
    async def unlaunch_uninstall(self, ctx):
        """Displays an embed with a link that tells you how to uninstalling Unlaunch"""
        embed = discord.Embed(title="Uninstalling Unlaunch")
        embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
        embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
        embed.url = "https://dsi.cfw.guide/uninstalling-unlaunch.html"
        embed.description = "How to uninstall Unlaunch on the DSi"
        await ctx.send(embed=embed)

    @uninstall.command(name="hiyacfw", aliases=["hiya"])
    async def hiyacfw_uninstall(self, ctx):
        """Displays an embed with a link that tells you how to uninstall hiyaCFW"""
        embed = discord.Embed(title="Uninstalling hiyaCFW")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.url = "https://wiki.ds-homebrew.com/hiyacfw/uninstalling.html"
        embed.description = "How to uninstall hiyaCFW on the DSi"
        await ctx.send(embed=embed)

    @commands.command()
    async def twlfix(self, ctx):
        """Information on how to fix a broken TWL Partition"""
        await self.simple_embed(ctx, """
                                Follow [TWLFix-CFW](https://github.com/MechanicalDragon0687/TWLFix-CFW/releases/).
                                These instructions require that you **perform a system update** after running the app.
                                """, title="Fix broken TWL")

    @commands.command()
    async def twlsettings(self, ctx):
        """How to access TWiLight Menu++ Settings"""
        embed = discord.Embed(title="How to access TWiLight Menu++ Settings")
        embed.description = "The way to access the TWiLight Menu++ settings varies between your configuration."
        embed.add_field(name="DS Classic Menu", value=cleandoc("""Hit the DS icon at the bottom of the lower screen"""), inline=False)
        embed.add_field(name="Nintendo DSi/SEGA Saturn/Homebrew Launcher themes using SELECT Menu", value=cleandoc("""Hit SELECT, then launch the Settings Applet (use the D-PAD to highlight options)"""), inline=False)
        embed.add_field(name="Nintendo DSi/SEGA Saturn/Homebrew Launcher themes not using SELECT Menu", value=cleandoc("""Hitting SELECT will bring you to the DS Classic Menu"""), inline=False)
        embed.add_field(name="Nintendo 3DS theme", value=cleandoc("""Use the touch screen to touch the wrench"""), inline=False)
        embed.add_field(name="R4 Original theme", value=cleandoc("""Hit START (if you’re in the file browser), then hit SELECT"""), inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["sd-card-setup", "sdformat"])
    async def formatsd(self, ctx):
        """Displays an embed with a link that tells you how to properly format your SD card"""
        embed = discord.Embed(title="SD Card Setup")
        embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
        embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
        embed.url = "https://dsi.cfw.guide/sd-card-setup.html"
        embed.description = "How to properly format your SD card"
        await ctx.send(embed=embed)

    @commands.command(aliases=["nanddump", "nandbackup"])
    async def nand(self, ctx):
        """Links to the NAND dumping guide"""
        embed = discord.Embed(title="Dumping NAND")
        embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
        embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
        embed.url = "https://dsi.cfw.guide/dumping-nand.html"
        embed.description = "How to dump your DSi's NAND"
        await ctx.send(embed=embed)

    @commands.command()
    async def vc(self, ctx):
        """Links to the 3DS Virtual Console Inject guide"""
        embed = discord.Embed(title="Virtual Console Injects for 3DS")
        embed.set_author(name="Asdolo")
        embed.set_thumbnail(url="https://i.imgur.com/rHa76XM.png")
        embed.url = "https://3ds.eiphax.tech/nsui.html"
        embed.description = "The recommended way to play old classics on your 3DS"
        await ctx.send(embed=embed)

    @commands.command()
    async def dump(self, ctx):
        """How to dump games and data for CFW consoles"""
        await self.simple_embed(ctx, text="""
                                    [Dumping DS cartridges from a 3DS console](https://3ds.hacks.guide/dumping-titles-and-game-cartridges#dumping-a-game-cartridge)
                                    [Dumping DS cartridges from a DSi console](https://dsi.cfw.guide/dumping-game-cards.html)
                                    [Dumping DSiWare](https://dsi.cfw.guide/dsiware-backups.html)
                                    """, title="Dumping Games to ROM files")

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def nightly(self, ctx):
        """Instructions on installing nightly builds"""
        await ctx.send_help(ctx.command)

    @nightly.command(name="twilight", aliases=twilightmenu_alias)
    async def twilight_nightly(self, ctx, *, arg=""):
        url = "https://github.com/TWLBot/Builds/raw/master/TWiLightMenu"
        console = ""
        if arg != "":
            if check_arg(arg, ("3ds",)):
                return await self.simple_embed(ctx, """
                                                    The latest nightly version of TWiLight Menu++ for 3DS can be downloaded from Universal Updater. \
                                                    Select TWiLight Menu++, then install the [nightly] build.
                                                    """, title="TWiLight Menu++ nightly for 3DS")
            elif check_arg(arg, ("dsi",)):
                url += "-DSi"
                console = "for DSi"
            elif check_arg(arg, ("flashcard", "flashcart", "ds")):
                url += "-Flashcard"
                console = "for flashcards"
        url += ".7z"
        description = f"The latest nightly version of TWiLight Menu++ {console} can be found here: {url}"
        if arg == "":
            description += "\n\nOn the 3DS, this can be installed from Universal Updater. Select TWiLight Menu++, then install the [nightly] build."
        await self.simple_embed(ctx, description, title=f"TWiLight Menu++ nightly {console}")

    @nightly.command(name="ndsbootstrap", aliases=ndsbootstrap_alias)
    async def ndsbootstrap_nightly(self, ctx, *, arg=""):
        url = "https://github.com/TWLBot/Builds/raw/master/nds-bootstrap.7z"
        description = f"The latest nightly version of nds-bootstrap can be found here: {url}\n\n\
                        On the 3DS, this can be installed from Universal Updater. Select nds-bootstrap, then install the [nightly] build."
        await self.simple_embed(ctx, description, title="nds-bootstrap nightly")

    @commands.group(aliases=["crowdin"], invoke_without_command=True, case_insensitive=True)
    async def translate(self, ctx):
        """Links to Crowdin projects"""
        await ctx.send_help(ctx.command)

    async def tlembed(self, ctx, title, extension):
        embed = discord.Embed(title=title + " Crowdin Project")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://support.crowdin.com/assets/logos/crowdin-white-symbol.png")
        embed.description = "Help translate " + title + " on Crowdin."
        embed.url = "https://crowdin.com/project/" + extension
        await ctx.send(embed=embed)

    @translate.command(aliases=twilightmenu_alias)
    async def twilight(self, ctx):
        await self.tlembed(ctx, "TWiLight Menu++", "TwilightMenu")

    @translate.command(aliases=ndsbootstrap_alias)
    async def ndsbootstrap(self, ctx):
        await self.tlembed(ctx, "nds-bootstrap", "nds-bootstrap")

    @translate.command(aliases=["skins", "ds-homebrew.com", "website"])
    async def wiki(self, ctx):
        await self.tlembed(ctx, "DS-Homebrew Wiki", "ds-homebrew-wiki")

    @translate.command(aliases=["dsicfwguide", "dsi.cfw.guide"])
    async def dsiguide(self, ctx):
        await self.tlembed(ctx, "DSi Guide", "dsi-guide")

    @commands.command(aliases=["colour"])
    async def color(self, ctx, *, color):
        """Displays conversions of a color from #RRGGBB, #RGB, RRR GGG BBB, and BGR15"""

        arg = color.replace("0x", "").replace("#", "")

        if len(arg) == 6:  # #RRGGBB
            rgb = int(arg[:2], 16), int(arg[2:4], 16), int(arg[4:6], 16)
        elif len(arg) == 3:  # #RGB
            rgb = (int(arg[0], 16) * 0x11, int(arg[1], 16) * 0x11, int(arg[2], 16) * 0x11)
        elif len(arg.split()) == 3:  # RRR GGG BBB
            split = arg.split()
            rgb = (max(min(int(split[0]), 0xFF), 0), max(min(int(split[1]), 0xFF), 0), max(min(int(split[2]), 0xFF), 0))
        elif len(arg) == 4:  # BGR15
            bgr15 = int(arg, 16)
            rgb = (round((bgr15 & 0x1F) * 0xFF / 0x1F), round(((bgr15 >> 5) & 0x1F) * 0xFF / 0x1F), round(((bgr15 >> 10) & 0x1F) * 0xFF / 0x1F))
        else:
            await ctx.send_help(ctx.command)
            return
        embed = discord.Embed(title="Color conversions")
        if ctx.invoked_with == "colour":
            embed.title = "Colour conversions"
        embed.color = rgb[0] << 0x10 | rgb[1] << 0x8 | rgb[2]
        embed.add_field(name="Hex (HTML)", value=f"`#{rgb[0] << 0x10 | rgb[1] << 0x8 | rgb[2]:06X}`")
        embed.add_field(name="RGB", value=f"`{rgb[0]} {rgb[1]} {rgb[2]}`")
        bgr15 = round(rgb[0] * 0x1F / 0xFF) | round(rgb[1] * 0x1F / 0xFF) << 5 | round(rgb[2] * 0x1F / 0xFF) << 10
        embed.add_field(name="BGR15", value=f"`0x{bgr15:04X}` `0x{bgr15 | 1 << 15:04X}`")
        await ctx.send(embed=embed)

    @commands.command()
    async def sdroot(self, ctx):
        """Displays an image that shows what a root is"""
        embed = discord.Embed()
        embed.set_image(url="https://media.discordapp.net/attachments/489307733074640926/756947922804932739/wherestheroot.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def sdlock(self, ctx):
        """Tells you how to disable write protection on an SD Card"""
        embed = discord.Embed(title="Disable write protection on an SD Card")
        embed.description = cleandoc("""
                                     This switch on the SD Card should be facing upwards, as in this photo. Otherwise, \
your device will refuse to write to it.
                                     *If it is write locked, your console and other applications may behave unexpectedly.*
                                     """)
        embed.set_image(url="https://i.imgur.com/RvKjWcz.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=["flashcard"])
    async def flashcart(self, ctx):
        """Links the r/flashcarts flashcart quick start guide"""
        embed = discord.Embed(title="Flashcart Quick Start Guide")
        embed.url = "https://www.reddit.com/r/flashcarts/wiki/ds-quick-start-guide"
        embed.description = "A Quick Guide on GBA and NDS flashcarts."
        embed.set_author(name="r/flashcarts")
        embed.set_thumbnail(url="https://b.thumbs.redditmedia.com/lBsOPXDyCx0p1MSx1qCdAtglHB4nineg5w9-3KHzO2A.png")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))

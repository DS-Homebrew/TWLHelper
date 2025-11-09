#
# Copyright (C) 2021-2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#
from __future__ import annotations

from inspect import cleandoc
from typing import Optional

import discord
from discord.ext import commands

from utils import (CustomView, Literal, build_wiki_embed, check_arg,
                   twilightmenu_alias)


class TWLMUIMenu(CustomView):
    def __init__(self, ctx, title, initDescription, themeSteps):
        self.message: Optional[discord.Message] = None
        self.themeSteps = themeSteps
        self.embed = discord.Embed(title=title)
        self.embed.description = initDescription
        super().__init__(ctx)

    def edit_embed(self, title, text):
        if not self.embed.fields:
            self.embed.add_field(name=title, value=cleandoc(text))
        else:
            self.embed.set_field_at(index=0, name=title, value=cleandoc(text))
        if self.embed.description:
            self.embed.description = None
        return

    @discord.ui.button(label="DSi/Saturn/HBL UI")
    async def dsi_button(self, itx, button):
        self.edit_embed("DSi/Saturn/HBL UI", self.themeSteps["dsi"])
        await itx.response.edit_message(embed=self.embed)

    @discord.ui.button(label="DS Classic Menu")
    async def ds_classic_button(self, itx, button):
        self.edit_embed("DS Classic Menu", self.themeSteps["ds"])
        await itx.response.edit_message(embed=self.embed)

    @discord.ui.button(label="3DS UI")
    async def _3ds_button_text(self, itx, button):
        self.edit_embed("3DS UI", self.themeSteps["3ds"])
        await itx.response.edit_message(embed=self.embed)

    @discord.ui.button(label="R4 UI")
    async def r4_button_text(self, itx, button):
        self.edit_embed("R4 UI", self.themeSteps["r4"])
        await itx.response.edit_message(embed=self.embed)

    @discord.ui.button(label="Wood UI")
    async def wood_button_text(self, itx, button):
        self.edit_embed("Wood UI", self.themeSteps["wood"])
        await itx.response.edit_message(embed=self.embed)

    async def start(self):
        self.message = await self.ctx.send(embed=self.embed, view=self)


class NDSCardFlagCheck():
    def __init__(self, inputFlags: int):
        self.inputFlags = inputFlags

    flags = {
        "MCCNT1_LATENCY1_SHIFT": 0,
        "MCCNT1_READ_DATA_DESCRAMBLE": (1 << 13),
        "MCCNT1_CLOCK_SCRAMBLER": (1 << 14),
        "MCCNT1_APPLY_SCRAMBLE_SEED": (1 << 15),
        "MCCNT1_CMD_SCRAMBLE": (1 << 22),
        "MCCNT1_DATA_READY": (1 << 23),
        "MCCNT1_CLK_6_7_MHZ": (0 << 27),
        "MCCNT1_CLK_4_2_MHZ": (1 << 27),
        "MCCNT1_LATENCY_CLK": (1 << 28),
        "MCCNT1_RESET_ON":  (0 << 29),
        "MCCNT1_RESET_OFF": (1 << 29),
        "MCCNT1_DIR_READ":  (0 << 30),
        "MCCNT1_DIR_WRITE": (1 << 30),
        "MCCNT1_ENABLE": (1 << 31)
    }

    flags_length = {
        "MCCNT1_LEN_0":     (0 << 24),
        "MCCNT1_LEN_512":   (1 << 24),
        "MCCNT1_LEN_1024":  (2 << 24),
        "MCCNT1_LEN_2048":  (3 << 24),
        "MCCNT1_LEN_4096":  (4 << 24),
        "MCCNT1_LEN_8192":  (5 << 24),
        "MCCNT1_LEN_16384": (6 << 24),
        "MCCNT1_LEN_4":     (7 << 24),
    }

    MCCNT1_LATENCY2_SHIFT = 16
    MCCNT1_LATENCY2_MASK = 0x3F0000

    def MCCNT1_LATENCY2(self, x) -> int:
        return (((x) << self.MCCNT1_LATENCY2_SHIFT) & self.MCCNT1_LATENCY2_MASK)

    def calculate(self) -> str:
        inputFlags = self.inputFlags
        result: int = 0

        valid_flags = []

        for i in reversed(self.flags):
            if inputFlags & self.flags[i]:
                valid_flags.append(i)
                result |= self.flags[i]
                inputFlags ^= self.flags[i]

        for i in reversed(range(63)):
            # Check equal instead of bitwise AND
            # this u8 is dedicated entirely to latency2
            if inputFlags & 0xFF0000 == self.MCCNT1_LATENCY2(i):
                valid_flags.append(f"MCCNT1_LATENCY2({i})")
                result |= self.MCCNT1_LATENCY2(i)
                inputFlags ^= self.MCCNT1_LATENCY2(i)
                break

        for i in self.flags_length:
            # Check equal instead of bitwise AND
            # this u8 is dedicated entirely to length
            if inputFlags & (0xFF << 24) == self.flags_length[i]:
                valid_flags.append(i)
                result |= self.flags_length[i]
                inputFlags ^= self.flags_length[i]
                break

        for i in reversed(range(0x1FFF)):
            # Check equal instead of bitwise AND
            # this u16 is dedicated entirely to latency1
            if inputFlags & 0x1FFF == i:
                valid_flags.append(f"MCCNT1_LATENCY1({i})")
                result |= i
                inputFlags ^= i
                break

        ret = ""
        for i in valid_flags:
            if valid_flags[-1] == i:
                ret += f"{i}"
            else:
                ret += f"{i} | "

        if inputFlags != 0:
            ret += f"\nUnknown flags: 0x{inputFlags:08X}"

        return ret


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

    @commands.command(require_var_positional=True, usage="<3ds|wiiu|vwii|switch|wii|dsi>")
    async def guide(self, ctx, guide: Literal("3ds", "wiiu", "vwii", "switch", "wii", "dsi")) -> None:  # noqa
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
            embed.set_author(name="Nintendo Homebrew")
            embed.set_thumbnail(url="https://i.imgur.com/KI6IXmm.png")
            embed.url = "https://wii.hacks.guide/"
            embed.description = "The complete guide to modding your Nintendo Wii"
            await ctx.send(embed=embed)
        elif check_arg(guide, 'dsi'):
            embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
            embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
            embed.url = "https://dsi.cfw.guide/"
            embed.description = "The complete guide to modding your Nintendo DSi"
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def install(self, ctx):
        """Links and/or information on installing apps"""
        await ctx.send_help(ctx.command)

    @install.command(name="twilight", aliases=twilightmenu_alias)
    async def twilight_install(self, ctx, twilight_install: Literal("addons", "noqa")) -> "noqa":
        if check_arg(twilight_install, 'addons'):
            embed = build_wiki_embed(title="TWiLight Menu++ Add-on Installation Guide", url="twilightmenu/installing-addons.html")
            embed.description = "How to install additional features to TWiLight Menu++"
            await ctx.send(embed=embed)
        elif check_arg(twilight_install, 'noqa'):
            embed = build_wiki_embed(title="TWiLight Menu++ Installation Guide", url="twilightmenu/installing.html")
            embed.description = "How to install TWiLight Menu++"
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="3DS", url="http://wiki.ds-homebrew.com/twilightmenu/installing-3ds.html"))
            view.add_item(discord.ui.Button(label="DSi", url="http://wiki.ds-homebrew.com/twilightmenu/installing-dsi.html"))
            view.add_item(discord.ui.Button(label="Flashcard", url="http://wiki.ds-homebrew.com/twilightmenu/installing-flashcard.html"))
            await ctx.send(embed=embed, view=view)

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

    @uninstall.command(name="twilight", aliases=twilightmenu_alias)
    async def twilight_uninstall(self, ctx):
        """Displays an embed with a link that tells you how to uninstall TWiLight Menu++ for a certain system."""
        embed = discord.Embed(title="TWiLight Menu++ Uninstall Guide")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.description = "How to uninstall TWiLight Menu++"
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="3DS", url="http://wiki.ds-homebrew.com/twilightmenu/uninstalling-3ds.html"))
        view.add_item(discord.ui.Button(label="DS & DSi", url="http://wiki.ds-homebrew.com/twilightmenu/uninstalling-ds.html"))
        await ctx.send(embed=embed, view=view)

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
    async def touchfix(self, ctx):
        """Information on how to fix broken touch input"""
        await self.simple_embed(ctx, """
                                For DSi users with Unlaunch, hold A+B buttons after pressing POWER, then select `Launcher`. If the issue persists or if Unlaunch is not installed, then re-insert the battery.
                                For 3DS users, follow [this guide](https://gbatemp.net/threads/recover-ds-mode-after-an-nvram-brick-eg-after-using-a-ds-bricker.516444/).
                                """, title="Fix broken touch input")

    @commands.command()
    async def twlfix(self, ctx):
        """Information on how to fix a broken TWL Partition"""
        await self.simple_embed(ctx, """
                                Follow [TWLFix-CFW](https://github.com/MechanicalDragon0687/TWLFix-CFW/releases/).
                                These instructions require that you **perform a system update** after running the app.
                                """, title="Fix broken TWL")

    @commands.command()
    async def twlmanual(self, ctx):
        """How to access TWiLight Menu++ Instruction Manual"""
        embed = discord.Embed(title="How to access TWiLight Menu++ Instruction Manual")
        embed.description = "To access TWiLight Menu++ Instruction Manual, follow the instructions relative to the way TWiLight Menu++ is setup on your device."
        embed.add_field(name="Nintendo DSi/SEGA Saturn/Homebrew Launcher UI", value=cleandoc("""Press the SELECT button\n- If you are met with a list of options, select **Open Manual**\n- If the screen turns white and then you are met with a different menu, follow the instructions for "**DS Classic Menu**" below"""), inline=False)
        embed.add_field(name="DS Classic Menu", value=cleandoc("""Tap the green book icon in the bottom right of the touchscreen"""), inline=False)
        embed.add_field(name="Nintendo 3DS UI", value=cleandoc("""Tap the green book icon in the top middle of the touchscreen"""), inline=False)
        embed.add_field(name="R4 Original UI", value=cleandoc("""In the main menu, tap the green book icon\n- If you are in the file explorer, press the START button to return to the main menu"""), inline=False)
        embed.add_field(name="Wood UI", value=cleandoc("""Press the START button or tap the START icon in the touchscreen\n- The screen should turn white and then you will be met with a different menu, follow the instructions for "**DS Classic Menu**" above"""), inline=False)
        embed.add_field(name="Online", value=cleandoc("""The TWiLight Menu++ manual is also available online at https://manual.ds-homebrew.com."""), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def twlsettings(self, ctx):
        """How to access TWiLight Menu++ Settings"""
        title = "How to access TWiLight Menu++ Settings"
        initDescription = "To access TWiLight Menu++ settings, follow the instructions relative to the way TWiLight Menu++ is setup on your device.\n- The console names do not represent the console you're using.\n- If this is your first time opening TWLMenu++ Settings, click on `DSi/Saturn/HBL UI`, as the DSi UI is used by default."
        themeSteps = {
            "dsi": """Press the SELECT button\n- If you are met with a list of options, select **TWLMenu++ Settings**\n- If the screen turns white and then you are met with a different menu, follow the instructions for "**DS Classic Menu**" below""",
            "ds": """Tap the small icon in the bottom center of the touchscreen""",
            "3ds": """Tap the icon in the top left corner of the touchscreen""",
            "r4": """In the main menu, press the SELECT button\n- If you are in the file explorer, press the START button to return to the main menu""",
            "wood": """Press the START button or tap the START icon in the touchscreen\n- The screen should turn white and then you will be met with a different menu, follow the instructions for "**DS Classic Menu**" below"""
        }
        view = TWLMUIMenu(ctx, title, initDescription, themeSteps)
        await view.start()

    @commands.command()
    async def slot1launch(self, ctx):
        """How to launch the Slot-1 Game Card from TWiLight Menu++"""
        title = "How to launch the Slot-1 Game Card from TWiLight Menu++"
        initDescription = "To launch the Slot-1 cartridge via TWiLight Menu++, follow the instructions relative to the way TWiLight Menu++ is setup on your device."
        themeSteps = {
            "dsi": """Press the SELECT button\n- If you are met with a list of options, select **Launch Slot-1 card**\n- If the screen turns white and then you are met with a different menu, follow the instructions for "**DS Classic Menu**" below""",
            "ds": """Tap the Slot-1 card on the center of the touchscreen""",
            "3ds": """Tap the Game Card icon at the top of the touchscreen""",
            "r4": """In the main menu, tap the center icon\n- If you are in the file explorer, press the START button to return to the main menu""",
            "wood": """Press the START button or tap the START icon in the touchscreen\n- The screen should turn white and then you will be met with a different menu, follow the instructions for "**DS Classic Menu**" below"""
        }
        view = TWLMUIMenu(ctx, title, initDescription, themeSteps)
        await view.start()

    @commands.command(aliases=["dsimenulaunch"])
    async def homemenulaunch(self, ctx):
        """How to launch the DSi Menu / 3DS HOME Menu from TWiLight Menu++"""
        title = "How to launch the DSi Menu / 3DS HOME Menu from TWiLight Menu++"
        initDescription = "To launch the DSi Menu / 3DS HOME Menu via TWiLight Menu++, follow the instructions relative to the way TWiLight Menu++ is setup on your device.\n- If you are using a 3DS, you may also use the HOME Menu button directly below the touchscreen"
        themeSteps = {
            "dsi": """Press the SELECT button\n- If you are met with a list of options, select **DSi Menu** / **3DS HOME Menu**\n- If the screen turns white and then you are met with a different menu, follow the instructions for \"**DS Classic Menu**\" below""",
            "ds": """Press X""",
            "3ds": """Tap the HOME icon at the top-right corner of the touchscreen""",
            "r4": """In the main menu, press B\n- If you are in the file explorer, press the START button to return to the main menu""",
            "wood": """Press the START button or tap the START icon in the touchscreen\n- The screen should turn white and then you will be met with a different menu, follow the instructions for "**DS Classic Menu**" below"""
        }
        view = TWLMUIMenu(ctx, title, initDescription, themeSteps)
        await view.start()

    @commands.command(aliases=["sd-card-setup", "sdformat"])
    async def formatsd(self, ctx):
        """Displays an embed with a link that tells you how to properly format your SD card"""
        embed = discord.Embed(title="SD Card Setup")
        embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
        embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
        embed.url = "https://dsi.cfw.guide/sd-card-setup.html"
        embed.description = "How to properly format your SD card\n\nThis setup guide must be followed, as it provides the proper tools to be used in order to format the SD card and/or check it for errors."
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

    @commands.command()
    async def nightly(self, ctx):
        """Instructions on installing nightly builds"""
        await ctx.send("Nightly builds are currently unavailable for DS-Homebrew projects.")

    @commands.command(aliases=["crowdin"])
    async def translate(self, ctx):
        """Links to Crowdin projects"""
        crowdin_baseurl = "https://crowdin.com/project"
        embed = discord.Embed(title="DS(i) Mode Hacking! Crowdin Projects")
        embed.set_author(name="DS-Homebrew")
        embed.set_thumbnail(url="https://support.crowdin.com/assets/logos/crowdin-white-symbol.png")
        embed.description = "Help translate our projects on Crowdin."
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="TWiLight Menu++", url=f"{crowdin_baseurl}/TwilightMenu"))
        view.add_item(discord.ui.Button(label="nds-bootstrap", url=f"{crowdin_baseurl}/nds-bootstrap"))
        view.add_item(discord.ui.Button(label="DS-Homebrew Wiki / Themes site", url=f"{crowdin_baseurl}/ds-homebrew-wiki"))
        view.add_item(discord.ui.Button(label="DSi Guide", url=f"{crowdin_baseurl}/dsi-guide"))
        await ctx.send(embed=embed, view=view)

    @commands.command(aliases=["colour"])
    async def color(self, ctx, *, color):
        """Displays conversions of a color from #RRGGBB, #RGB, RRR GGG BBB, and BGR15"""

        arg = color.replace("0x", "").replace("#", "")

        try:
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
                return await ctx.send_help(ctx.command)
        except ValueError:
            return await ctx.send_help(ctx.command)
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

    @commands.group(aliases=["flashcard", "flashcards", "flashcarts"], invoke_without_command=True, case_insensitive=True)
    async def flashcart(self, ctx):
        """Links the Flashcarts Wiki quick start guide for a given console"""
        await ctx.send_help(ctx.command)

    @flashcart.command(aliases=["nds", "dsi", "3ds"])
    async def ds(self, ctx):
        """Links the Flashcarts Wiki DS flashcart quick start guide"""
        embed = discord.Embed(title="DS Flashcart Quick Start Guide")
        embed.url = "https://flashcarts.net/ds-quick-start-guide.html"
        embed.description = "A Quick Guide on DS Flashcarts"
        embed.set_author(name="The Flashcarts Wiki")
        embed.set_thumbnail(url="https://flashcarts.net/assets/images/favicon/favicon-196x196.png")
        await ctx.send(embed=embed)

    @flashcart.command()
    async def gba(self, ctx):
        """Links the Flashcarts Wiki  GBA flashcart quick start guide"""
        embed = discord.Embed(title="GBA Flashcart Quick Start Guide")
        embed.url = "https://flashcarts.net/gba-quick-start-guide.html"
        embed.description = "A Quick Guide on GBA Flashcarts"
        embed.set_author(name="The Flashcarts Wiki")
        embed.set_thumbnail(url="https://flashcarts.net/assets/images/favicon/favicon-196x196.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=["twlboot"])
    async def dsiboot(self, ctx):
        """Tells you how to automatically boot TWiLight Menu++ with Unlaunch"""
        embed = discord.Embed(title="How to launch TWiLight Menu++ automatically with Unlaunch")
        embed.description = cleandoc("""
                                    In Unlaunch, select `Options`, then set `TWiLight Menu++` (`boot.nds`) as `No Button`, select `Save & Exit`, and reboot.
                                    If you do not know how to open Unlaunch, **turn your DSi completely off**, \
**hold** `A` and `B` together and press power **while** holding said buttons.\n
                                    If done correctly, your DSi should automatically boot into TWiLight Menu++.
                                    """)
        await ctx.send(embed=embed)

    @commands.command(name="7-zip", aliases=["7zip", "7z"])
    async def sevenzip(self, ctx):
        """Links to the 7-Zip website"""
        embed = discord.Embed(title="7-Zip")
        embed.url = "https://www.7-zip.org/"
        embed.description = "7-Zip is the recommended program for Windows users to use to extract .7z files, such as the one TWiLight Menu++ comes in.\nMost people should download the '64-bit x64' version."
        await ctx.send(embed=embed)

    @commands.command()
    async def ysmenu(self, ctx):
        """Links to RetroGameFan's YSMenu download page"""
        embed = discord.Embed(title="RetroGameFan's YSMenu")
        embed.url = "https://gbatemp.net/download/35737/"
        embed.description = "Kernel for the DSTT family of flash cartridges"
        embed.set_author(name="Yasu Software & RetroGameFan")
        embed.set_thumbnail(url="https://gbatemp.net/data/avatars/l/221/221134.jpg?1570890734")
        await ctx.send(embed=embed)

    @commands.command()
    async def lazydsi(self, ctx):
        """Tells you to stop trying to use it (and/or the vguide)"""
        embed = discord.Embed(title="Lazy DSi Downloader is deprecated")
        embed.description = "This application is deprecated. Please read the [guide](https://dsi.cfw.guide)."
        await ctx.send(embed=embed)

    @commands.command()
    async def cardflagcheck(self, ctx, inputFlags: str):
        try:
            card = NDSCardFlagCheck(int(inputFlags, 16))
        except ValueError:
            return await ctx.send("Input is not a valid hex number. Please try again.")
        await ctx.send(f"0x{card.inputFlags:08X} = {card.calculate()}")

    @commands.command()
    async def blockconvert(self, ctx, blocks: int):
        """Converts Nintendo Blocks to normal storage units. 1 block == 128 KiB"""
        kibibytes = blocks << 7  # 1 block == 128 KiB
        ret = f"{kibibytes} KiB"
        if kibibytes > 1048576:  # over 1 GiB
            ret = f"{kibibytes >> 20} GiB"
        elif kibibytes > 1024:  # over 1 MiB
            ret = f"{kibibytes >> 10} MiB"

        await ctx.send(f"{blocks} blocks is equivalent to {ret}.")


async def setup(bot):
    await bot.add_cog(General(bot))

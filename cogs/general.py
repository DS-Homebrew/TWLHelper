import discord

from discord.ext import commands
from inspect import cleandoc


class General(commands.Cog):
    """
    General commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.systems = ("3ds", "wiiu", "vwii", "switch", "nx", "ns", "wii", "dsi")

    async def simple_embed(self, ctx, text, *, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = cleandoc(text)
        await ctx.send(embed=embed)

    def check_arg(self, message, arg):
        message = message.lower()
        if message in arg:
            return True
        return False

    @commands.command()
    async def guide(self, ctx, *, arg=""):
        """Links to the recommended guides"""
        arg = arg.casefold()
        arglist = {x for x in arg.split() if x in self.systems}

        if arg not in self.systems:
            await ctx.send(f"Please specify a console. Valid options are: {', '.join([x for x in self.systems])}.")
            return

        embed = discord.Embed(title="Guide")
        for x in arglist:
            if self.check_arg(x, '3ds'):
                embed.set_author(name="Nintendo Homebrew & Plailect")
                embed.set_thumbnail(url="https://nintendohomebrew.com/pics/nhplai.png")
                embed.url = "https://3ds.hacks.guide/"
                embed.description = "3DS Hacks Guide"
                await ctx.send(embed=embed)
                continue
            if self.check_arg(x, ('wiiu',)):
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/CVSu1zc.png")
                embed.url = "https://wiiu.hacks.guide/"
                embed.description = "Wii U Hacks Guide"
                await ctx.send(embed=embed)
                continue
            if self.check_arg(x, ('vwii',)):
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/FclGzNz.png")
                embed.url = "https://wiiu.hacks.guide/#/vwii-modding"
                embed.description = "vWii modding guide"
                await ctx.send(embed=embed)
                continue
            if self.check_arg(x, ('switch', 'nx', 'ns')):
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/CVSu1zc.png")
                embed.url = "https://nh-server.github.io/switch-guide/"
                embed.description = "Switch hacking guide"
                await ctx.send(embed=embed)
                continue
            if self.check_arg(x, 'wii'):
                embed.set_author(name="RiiConnect24")
                embed.set_thumbnail(url="https://i.imgur.com/KI6IXmm.png")
                embed.url = "https://wii.guide/"
                embed.description = "Wii softmod guide"
                await ctx.send(embed=embed)
            if self.check_arg(x, 'dsi'):
                embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
                embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
                embed.url = "https://dsi.cfw.guide/"
                embed.description = "DSi CFW Guide"
                await ctx.send(embed=embed)

    @commands.command()
    async def twlfix(self, ctx):
        """Information on how to fix a broken TWL Partition"""
        await self.simple_embed(ctx, """
                                If you are encountering black screen on a 3DS family console while using DS-mode applications, \
                                use [TWLFix-CFW](https://github.com/MechanicalDragon0687/TWLFix-CFW/releases/) to fix it.
                                """, title="Fix broken TWL")

    @commands.command()
    async def unlaunch(self, ctx):
        """Installing Unlaunch"""
        embed = discord.Embed(title="Installing Unlaunch")
        embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
        embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
        embed.url = "https://dsi.cfw.guide/installing-unlaunch.html"
        embed.description = "How to install Unlaunch on the DSi"
        await ctx.send(embed=embed)

    @commands.command(alias=["sd-card-setup", "sdformat"])
    async def formatsd(self, ctx):
        """Formatting your SD card"""
        embed = discord.Embed(title="SD Card Setup")
        embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
        embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
        embed.url = "https://dsi.cfw.guide/sd-card-setup.html"
        embed.description = "How to properly format your DSi's SD card"
        await ctx.send(embed=embed)

    @commands.command()
    async def dump(self, ctx, arg=None):
        """How to dump games and data for CFW consoles"""
        systems = ("3ds", "dsi")

        if arg not in systems:
            await ctx.send(f"Please specify a console. Valid options are: {', '.join([x for x in systems])}.")
            return

        if self.check_arg(arg, '3ds'):
            embed = discord.Embed(title="GodMode9 Dump Guide")
            embed.set_author(name="Nintendo Homebrew & Plailect", url="https://3ds.hacks.guide/dumping-titles-and-game-cartridges")
            embed.set_thumbnail(url="https://nintendohomebrew.com/pics/nhplai.png")
            embed.url = "https://3ds.hacks.guide/dumping-titles-and-game-cartridges.html"
            embed.description = "How to dump Cartridges and Files on a 3DS using GodMode9"
            await ctx.send(embed=embed)
        elif self.check_arg(arg, 'dsi'):
            embed = discord.Embed(title="GodMode9i Dump Guide")
            embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking", url="https://dsi.cfw.guide/dumping-game-cards")
            embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
            embed.url = "https://dsi.cfw.guide/dumping-game-cards.html"
            embed.description = "How to dump cartridges on a Nintendo DSi using GodMode9i"
            await ctx.send(embed=embed)

    @commands.group(aliases=["crowdin"], invoke_without_command=True, case_insensitive=True)
    async def translate(self, ctx):
        """Links to Crowdin projects"""
        await ctx.send_help(ctx.command)

    def tlembed(self, title):
        embed = discord.Embed(title=title + " Crowdin Project")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://support.crowdin.com/assets/logos/crowdin-white-symbol.png")
        embed.description = "Help translate " + title + " on Crowdin."
        embed.url = "https://crowdin.com/project/"
        return embed

    @translate.command(aliases=["twlmenu", "twl", "twilightmenu"])
    async def twilight(self, ctx):
        embed = self.tlembed("TWiLight Menu++")
        embed.url += "TwilightMenu"  # Don't add .html, it breaks the link
        await ctx.send(embed=embed)

    @translate.command(aliases=["nds-bootstrap", "bootstrap", "ndsbs", "bs"])
    async def ndsbootstrap(self, ctx):
        embed = self.tlembed("nds-bootstrap")
        embed.url += "nds-bootstrap"  # Don't add .html, it breaks the link
        await ctx.send(embed=embed)

    @translate.command(aliases=["skins", "ds-homebrew.com", "website"])
    async def wiki(self, ctx):
        embed = self.tlembed("DS-Homebrew Wiki")
        embed.url += "ds-homebrew-wiki"  # Don't add .html, it breaks the link
        await ctx.send(embed=embed)

    @translate.command(aliases=["dsicfwguide", "dsi.cfw.guide"])
    async def dsiguide(self, ctx):
        embed = self.tlembed("DSi Guide")
        embed.url += "dsi-guide"  # Don't add .html, it breaks the link
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))

import discord

from discord.ext import commands
from inspect import cleandoc


class Assistance(commands.Cog):
    """
    Commands that assist
    """

    def __init__(self, bot):
        self.bot = bot
        self.systems = ("3ds", "wiiu", "vwii", "switch", "nx", "ns", "wii", "dsi")

    async def simple_embed(self, ctx, text, *, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = cleandoc(text)
        await ctx.send(embed=embed)

    def check_console(self, message, consoles):
        message = message.lower()
        if message in consoles:
            return True
        return False

    @commands.command()
    async def guide(self, ctx, *, consoles=""):
        """Links to the recommended guides."""
        consoles = consoles.casefold()
        consoleslist = {x for x in consoles.split() if x in self.systems}

        if not consoleslist:
            await ctx.send(f"Please specify a console. Valid options are: {', '.join([x for x in self.systems])}.")

            ctx.command.reset_cooldown(ctx)
            return
        for x in consoleslist:
            if self.check_console(x, '3ds'):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="Nintendo Homebrew & Plailect")
                embed.set_thumbnail(url="https://nintendohomebrew.com/pics/nhplai.png")
                embed.url = "https://3ds.hacks.guide/"
                embed.description = "3DS Hacks Guide"
                await ctx.send(embed=embed)
                continue
            if self.check_console(x, ('wiiu',)):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/CVSu1zc.png")
                embed.url = "https://wiiu.hacks.guide/"
                embed.description = "Wii U Hacks Guide"
                await ctx.send(embed=embed)
                continue
            if self.check_console(x, ('vwii',)):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/FclGzNz.png")
                embed.url = "https://wiiu.hacks.guide/#/vwii-modding"
                embed.description = "vWii modding guide"
                await ctx.send(embed=embed)
                continue
            if self.check_console(x, ('switch', 'nx', 'ns')):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/CVSu1zc.png")
                embed.url = "https://nh-server.github.io/switch-guide/"
                embed.description = "Switch hacking guide"
                await ctx.send(embed=embed)
                continue
            if self.check_console(x, 'wii'):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="RiiConnect24")
                embed.set_thumbnail(url="https://i.imgur.com/KI6IXmm.png")
                embed.url = "https://wii.guide/"
                embed.description = "Wii softmod guide"
                await ctx.send(embed=embed)
            if self.check_console(x, 'dsi'):
                embed = discord.Embed(title="Guide")
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

    @commands.group(aliases=["howto"], invoke_without_command=True, case_insensitive=True)
    async def tutorial(self, ctx):
        """Links to one of multiple guides"""
        await ctx.send_help(ctx.command)

    @tutorial.command()
    async def widescreen(self, ctx):
        """Widescreen for 3DS TWLMenu++"""
        embed = discord.Embed(title="Playing in Widescreen")
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/playing-in-widescreen.html"
        embed.description = "Playing in widescreen with TWiLight Menu++ on 3DS"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Assistance(bot))

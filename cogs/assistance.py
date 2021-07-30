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

    def check_arg(self, message, arg):
        message = message.lower()
        if message in arg:
            return True
        return False

    @commands.command()
    async def guide(self, ctx, *, arg=""):
        """Links to the recommended guides."""
        arg = arg.casefold()
        arglist = {x for x in arg.split() if x in self.systems}

        if not arglist:
            await ctx.send(f"Please specify a console. Valid options are: {', '.join([x for x in self.systems])}.")
            return
        for x in arglist:
            if self.check_arg(x, '3ds'):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="Nintendo Homebrew & Plailect")
                embed.set_thumbnail(url="https://nintendohomebrew.com/pics/nhplai.png")
                embed.url = "https://3ds.hacks.guide/"
                embed.description = "3DS Hacks Guide"
                await ctx.send(embed=embed)
                continue
            if self.check_arg(x, ('wiiu',)):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/CVSu1zc.png")
                embed.url = "https://wiiu.hacks.guide/"
                embed.description = "Wii U Hacks Guide"
                await ctx.send(embed=embed)
                continue
            if self.check_arg(x, ('vwii',)):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/FclGzNz.png")
                embed.url = "https://wiiu.hacks.guide/#/vwii-modding"
                embed.description = "vWii modding guide"
                await ctx.send(embed=embed)
                continue
            if self.check_arg(x, ('switch', 'nx', 'ns')):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="Nintendo Homebrew")
                embed.set_thumbnail(url="https://i.imgur.com/CVSu1zc.png")
                embed.url = "https://nh-server.github.io/switch-guide/"
                embed.description = "Switch hacking guide"
                await ctx.send(embed=embed)
                continue
            if self.check_arg(x, 'wii'):
                embed = discord.Embed(title="Guide")
                embed.set_author(name="RiiConnect24")
                embed.set_thumbnail(url="https://i.imgur.com/KI6IXmm.png")
                embed.url = "https://wii.guide/"
                embed.description = "Wii softmod guide"
                await ctx.send(embed=embed)
            if self.check_arg(x, 'dsi'):
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


def setup(bot):
    bot.add_cog(Assistance(bot))

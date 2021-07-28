import discord

from discord.ext import commands

class Wiki(commands.Cog):
    """
    Commands that link to wiki pages
    """

    def __init__(self, bot):
        self.bot = bot

    async def simple_embed(self, ctx, text, *, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = cleandoc(text)
        await ctx.send(embed=embed)

    @commands.group(cooldown=commands.Cooldown(0, 0, commands.BucketType.channel), invoke_without_command=True, case_insensitive=True)
    async def faq(self, ctx, *, consoles=""):
        """Links to the FAQ for an application."""
        await ctx.send_help(ctx.command)

    @faq.command(aliases=["twl"], cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def twilight(self, ctx):
        embed = discord.Embed(title="TWiLight Menu++")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/faq"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        await ctx.send(embed=embed)
    
    @faq.command(cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def ndsbootstrap(self, ctx):
        embed = discord.Embed(title="nds-bootstrap")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/nds-bootstrap/faq"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        await ctx.send(embed=embed)

    @faq.command(cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def gbarunner2(self, ctx):
        embed = discord.Embed(title="GBARunner2")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/gbarunner2/faq"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        await ctx.send(embed=embed)
    @faq.command(aliases=["hiya"], cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def hiyacfw(self, ctx):
        embed = discord.Embed(title="hiyaCFW")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/hiyacfw/faq"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))

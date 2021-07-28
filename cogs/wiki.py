import discord

from discord.ext import commands

class Wiki(commands.Cog):
    """
    Commands that link to wiki pages
    """

    def __init__(self, bot):
        self.bot = bot
        self.applications = ("twilight", "twl", "nds-bootstrap", "gbarunner2", "hiyacfw")

    async def simple_embed(self, ctx, text, *, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = cleandoc(text)
        await ctx.send(embed=embed)

    def check_application(self, message, applications):
        message = message.lower()
        if message in applications:
            return True
        return False

    @commands.command()
    async def faq(self, ctx, *, applications=""):
        """Links to the FAQ for an application."""
        applications = applications.casefold()
        applist = {x for x in applications.split() if x in self.applications}

        if not applist:
            await ctx.send(f"Please specify an application. Valid options are: {', '.join([x for x in self.applications])}.")

            ctx.command.reset_cooldown(ctx)
            return
        for x in applist:
            if self.check_application(x, ('twilight', 'twl')):
                embed = discord.Embed(title="TWiLight Menu++")
                embed.set_author(name="DS-Homebrew", url="https://wiki.ds-homebrew.com/")
                embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
                embed.url = "https://wiki.ds-homebrew.com/twilightmenu/faq"
                embed.description = "Frequently Asked Questions & Troubleshooting"
                await ctx.send(embed=embed)
                continue
            if self.check_application(x, 'nds-bootstrap'):
                embed = discord.Embed(title="nds-bootstrap")
                embed.set_author(name="DS-Homebrew", url="https://wiki.ds-homebrew.com/")
                embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
                embed.url = "https://wiki.ds-homebrew.com/nds-bootstrap/faq"
                embed.description = "Frequently Asked Questions & Troubleshooting"
                await ctx.send(embed=embed)
                continue
            if self.check_application(x, 'gbarunner2'):
                embed = discord.Embed(title="GBARunner2")
                embed.set_author(name="DS-Homebrew", url="https://wiki.ds-homebrew.com/")
                embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
                embed.url = "https://wiki.ds-homebrew.com/gbarunner2/faq"
                embed.description = "Frequently Asked Questions & Troubleshooting"
                await ctx.send(embed=embed)
                continue
            if self.check_application(x, 'hiyacfw'):
                embed = discord.Embed(title="TWiLight Menu++")
                embed.set_author(name="DS-Homebrew", url="https://wiki.ds-homebrew.com/")
                embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
                embed.url = "https://wiki.ds-homebrew.com/hiyacfw/faq"
                embed.description = "Frequently Asked Questions & Troubleshooting"
                await ctx.send(embed=embed)
                continue


def setup(bot):
    bot.add_cog(Wiki(bot))

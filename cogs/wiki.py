import discord

from discord.ext import commands

class Wiki(commands.Cog):
    """
    Commands that link to wiki pages
    """

    def __init__(self, bot):
        self.bot = bot

    def check_arg(self, message, arg):
        message = message.lower()
        if message in arg:
            return True
        return False

    async def simple_embed(self, ctx, text, *, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = cleandoc(text)
        await ctx.send(embed=embed)

    def web_name(self, name):
        name = name.lower()
        out = ""
        for letter in name:
            if letter in "abcdefghijklmnopqrstuvwxyz0123456789-_.":
                out += letter
            elif letter == " ":
                out += "-"
        return out

    @commands.group(cooldown=commands.Cooldown(0, 0, commands.BucketType.channel), invoke_without_command=True, case_insensitive=True)
    async def faq(self, ctx):
        """Links to the FAQ for an application."""
        await ctx.send_help(ctx.command)

    @faq.command(aliases=["twl"], cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def twilight(self, ctx, *, arg=""):
        faqs = (
            "Why does my 3DS/2DS get stuck on black screens, crash, power off, etc when launching TWiLight Menu++?",
            "TWL_FIRM might’ve somehow got corrupted. Follow this guide to fix the issue: https://3ds.hacks.guide/troubleshooting#dsi--ds-functionality-is-broken-after-completing-the-guide",
            "How do I fix getting a white screen when booting TWiLight Menu++?",
            "Where is the Acekard/Wood UI theme?",
            "How do I fix TWiLight Menu++ restarting or giving a Guru Meditation Error when launching a game?",
            "Why do I get a white screen when trying to load a game from SD card?",
            "How do I use cheats?",
            "How do I show a custom picture on the top screen of the DSi theme?",
            "How do I get games?",
            "Can I get the save files from my game cards onto my SD card or vice versa?",
            "How do I change TWiLight Menu++’s language?",
            "Is this a DS(i) emulator?",
            "What systems does TWiLight Menu++ support?",
            "Why isn’t touch input working on sudokuhax?",
            "Can The Biggest Loser boot TWiLight Menu++?"
        )

        embed = discord.Embed(title="TWiLight Menu++ FAQ")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/twilightmenu/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"

        if arg != "":
            for faq in faqs:
                if arg.lower() in faq.lower():
                    embed.url = embed.url + "?faq=" + self.web_name(faq)
                    embed.description = faq

        await ctx.send(embed=embed)
    
    @faq.command(cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def ndsbootstrap(self, ctx, *, arg=""):
        faqs = (
            "nds-bootstrap FAQ & Troubleshooting",
            "Why do I get a white screen when trying to load a game from SD card?",
            "nds-bootstrap troubleshooting",
            "Why are there issues with ROM loading, even though they’re run natively?",
            "Why use nds-bootstrap over a regular flashcard?",
            "Donor ROMs",
            "What is a nightly and where do I get it?",
            "Why do my cheats not work?",
        )

        embed = discord.Embed(title="nds-bootstrap FAQ")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/nds-bootstrap/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"

        if arg != "":
            for faq in faqs:
                if arg.lower() in faq.lower():
                    embed.url = embed.url + "?faq=" + self.web_name(faq)
                    embed.description = faq

        await ctx.send(embed=embed)

    @faq.command(cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def gbarunner2(self, ctx, *, arg=""):
        faqs = (
            "How do I create and add custom borders?",
            "Are cheats supported?",
            "How do I use nightly GBARunner2 builds in TWiLight Menu++?",
            "How do I use Wi-Fi link features?",
        )

        embed = discord.Embed(title="GBARunner2 FAQ")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/gbarunner2/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"

        if arg != "":
            for faq in faqs:
                if arg.lower() in faq.lower():
                    embed.url = embed.url + "?faq=" + self.web_name(faq)
                    embed.description = faq

        await ctx.send(embed=embed)

    @faq.command(aliases=["hiya"], cooldown=commands.Cooldown(0, 0, commands.BucketType.channel))
    async def hiyacfw(self, ctx):
        embed = discord.Embed(title="hiyaCFW Troubleshooting")
        embed.set_author(name="DS-Homebrew Wiki", url="https://wiki.ds-homebrew.com/")
        embed.set_thumbnail(url="https://wiki.ds-homebrew.com/assets/images/favicon/apple-icon-180x180.png")
        embed.url = "https://wiki.ds-homebrew.com/hiyacfw/troubleshooting.html"
        embed.description = "Troubleshooting"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))

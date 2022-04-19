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
import re
from typing import Optional

import discord
from discord.ext import commands

from utils import ndsbootstrap_alias, twilightmenu_alias, web_name


class FAQ(commands.Cog):
    """
    Commands that link to FAQ pages
    """

    def __init__(self, bot):
        self.bot = bot

    descriptionMaxSize = 750

    def wikiembed(self, title):
        embed = discord.Embed(title=title)
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        embed.url = "https://wiki.ds-homebrew.com/"
        return embed

    async def read_faq(self, ctx, console, arg, embed):
        page = None
        r = await self.bot.session.get(f"https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/{console.lower()}/faq.md")
        if r.status == 200:
            page = await r.text()
        else:
            return await ctx.send(embed=embed)
        faqpage = page.splitlines()
        itera = 0
        field_title = None
        for faq in faqpage:
            itera += 1
            if arg.lower() in faq.lower() and "#### " in faq.lower():
                field_title = faq[5:]
                embed.url += f"?faq={web_name(field_title)}"
                embed.description = None
                break
        if embed.description:
            return await ctx.send(embed=embed)
        line = faqpage[itera]
        field_description = ""
        while "#### " not in line or "#####" in line:
            field_description += '\n' + faqpage[itera]
            itera += 1
            if itera < len(faqpage):
                line = faqpage[itera]
            else:
                break
        field_description = re.sub("##### (.*)", "**\\1**", field_description)  # Change h5 to bold
        field_description = re.sub("<kbd(?: class=\"[^\"]*\")?>(.*?)</kbd>", "`\\1`", field_description)  # Change kbd to inline code
        field_description = re.sub("<.*?>(.*?)</.*?>", "\\1", field_description)  # Remove other HTML
        field_description = re.sub("<(area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr).*?>", "[\\1]", field_description)  # Remove self-closing HTML
        embed.description = f"**{field_title}**"
        if len(embed.description) + len(field_description) > self.descriptionMaxSize:
            embed.description += "\nSee linked page for details."
        else:
            embed.description += field_description
        await ctx.send(embed=embed)

    async def read_guide(self, ctx, arg, embed):
        page = None
        r = await self.bot.session.get("https://raw.githubusercontent.com/cfw-guide/dsi.cfw.guide/master/docs/faq.md")
        if r.status == 200:
            page = await r.text()
        else:
            return await ctx.send(embed=embed)
        faqpage = page.splitlines()
        itera = 0
        field_title = None
        for faq in faqpage:
            itera += 1
            if arg.lower() in faq.lower() and "## " in faq.lower():
                field_title = faq[3:]
                embed.url += f"#{web_name(field_title)}"
                embed.description = None
                break
        if embed.description:
            return await ctx.send(embed=embed)
        line = faqpage[itera]
        field_description = ""
        while "## " not in line or "###" in line:
            field_description += '\n' + faqpage[itera]
            itera += 1
            if itera < len(faqpage):
                line = faqpage[itera]
            else:
                break
        field_description = re.sub("##### (.*)", "**\\1**", field_description)  # Change h5 to bold
        field_description = re.sub("<kbd(?: class=\"[^\"]*\")?>(.*?)</kbd>", "`\\1`", field_description)  # Change kbd to inline code
        field_description = re.sub("<.*?>(.*?)</.*?>", "\\1", field_description)  # Remove other HTML
        field_description = re.sub("<(area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr).*?>", "[\\1]", field_description)  # Remove self-closing HTML
        embed.description = f"**{field_title}**"
        if len(embed.description) + len(field_description) > self.descriptionMaxSize:
            embed.description += "\nSee linked page for details."
        else:
            embed.description += field_description
        await ctx.send(embed=embed)

    def read_glossary(self, file, iter):
        line = file[iter]
        out = ""
        while "### " not in line or "####" in line:
            out += '\n' + file[iter]
            iter += 1
            if iter < len(file):
                line = file[iter]
            else:
                break
        out = re.sub("#### (.*)", "**\\1**", out)  # Change h4 to bold
        out = re.sub("<kbd(?: class=\"[^\"]*\")?>(.*?)</kbd>", "`\\1`", out)  # Change kbd to inline code
        out = re.sub("<(.*?)>(.*?)<\\/\\1>", "\\2", out)  # Remove other HTML
        out = re.sub("<(area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr).*?>", "[\\1]", out)  # Remove self-closing HTML
        return out

    @commands.hybrid_group(invoke_without_command=True, case_insensitive=True, fallback="all")
    async def faq(self, ctx):
        """Links to the FAQ for an application"""
        await ctx.send_help(ctx.command)

    @faq.command(name="twilight", aliases=twilightmenu_alias)
    async def twilight_faq(self, ctx, *, query: Optional[str] = None):
        """Shows a FAQ entry from the wiki regarding TWiLight Menu++"""
        embed = self.wikiembed("TWiLight Menu++ FAQ")
        embed.url += "twilightmenu/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if not query:
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "twilightmenu", query, embed)

    @faq.command(aliases=ndsbootstrap_alias)
    async def ndsbootstrap(self, ctx, *, query: Optional[str] = None):
        """Shows a FAQ entry from the wiki regarding nds-bootstrap"""
        embed = self.wikiembed("nds-bootstrap FAQ")
        embed.url += "nds-bootstrap/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if not query:
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "nds-bootstrap", query, embed)

    @faq.command(aliases=["gbar2"])
    async def gbarunner2(self, ctx, *, query: Optional[str] = None):
        """Shows a FAQ entry from the wiki regarding GBARunner2"""
        embed = self.wikiembed("GBARunner2 FAQ")
        embed.url += "gbarunner2/faq.html"
        if not query:
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "gbarunner2", query, embed)

    @faq.command(aliases=["gm9i"])
    async def godmode9i(self, ctx, *, query: Optional[str] = None):
        """Shows a FAQ entry from the wiki regarding GodMode9i"""
        embed = self.wikiembed("GodMode9i FAQ")
        embed.url += "godmode9i/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if not query:
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "godmode9i", query, embed)

    @faq.command(aliases=["hiya"])
    async def hiyacfw(self, ctx, *, query: Optional[str] = None):
        """Displays an embed with a link to the hiyaCFW FAQ"""
        embed = self.wikiembed("hiyaCFW FAQ")
        embed.url += "hiyacfw/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if not query:
            await ctx.send(embed=embed)
        else:
            await self.read_faq(ctx, "hiyacfw", query, embed)

    @faq.command(name="guide")
    async def faq_guide(self, ctx, *, query: Optional[str] = None):
        """Shows a FAQ entry from the DSi CFW Guide"""
        embed = discord.Embed(title="DSi Guide FAQ")
        embed.set_author(name="emiyl & DS⁽ⁱ⁾ Mode Hacking")
        embed.set_thumbnail(url="https://i.imgur.com/OGelKVt.png")
        embed.url = "https://dsi.cfw.guide/faq.html"
        embed.description = "Frequently Asked Questions & Troubleshooting"
        if not query:
            await ctx.send(embed=embed)
        else:
            await self.read_guide(ctx, query, embed)

    @commands.hybrid_command()
    async def glossary(self, ctx, *, arg: Optional[str]=None):
        """nds-bootstrap Glossary"""
        embed = self.wikiembed("nds-bootstrap Glossary")
        embed.url += "nds-bootstrap/glossary.html"
        embed.description = "Glossary for nds-bootstrap"
        if not arg:
            await ctx.send(embed=embed)
            return
        
        r = await self.bot.session.get("https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/nds-bootstrap/glossary.md")
        if r.status == 200:
            page = await r.text()
        else:
            await ctx.send(embed=embed)
            return

        glossary = page.splitlines()
        itera = 0
        for item in glossary:
            itera += 1
            if arg.lower() in item.lower() and "### " in item.lower():
                title = item[4:]
                embed.url += f"#{web_name(title)}"
                embed.description = None
                embed.add_field(name=title, value=self.read_glossary(glossary, itera))
                break
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(FAQ(bot))

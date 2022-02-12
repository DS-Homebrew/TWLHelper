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
import hashlib
import feedparser
import os

from discord.ext import tasks, commands
from inspect import cleandoc
from time import asctime
from bs4 import BeautifulSoup

import settings


class RSS(commands.Cog):
    """RSS feeds"""

    def __init__(self, bot):
        self.bot = bot
        self.loop.start()

    @tasks.loop(seconds=600)
    async def loop(self):
        await self.bot.wait_until_ready()
        if settings.NINUPDATE:
            await self.ninupdates()
        if settings.SUBREDDIT:
            await self.subreddit()

    def digest_check(self, new, old):
        digestprev = hashlib.sha256(old).digest()
        digestnext = hashlib.sha256(new).digest()
        return digestprev == digestnext

    def parse_feed(self, new, old):
        feed = {}
        feed['new'] = feedparser.parse(new)
        feed['old'] = feedparser.parse(old)
        return feed

    async def ninupdates(self):
        async with self.bot.session.get('https://yls8.mtheall.com/ninupdates/feed.php') as resp:
            raw_bytes = await resp.read()

        if not os.path.isfile('ninupdates.xml'):
            new = open('ninupdates.xml', 'wb')
            new.write(raw_bytes)
            new.close()

        f = open('ninupdates.xml', 'rb')
        if not self.digest_check(raw_bytes, f.read()):
            f.close()

            consoles = [
                'Old3DS',
                'New3DS'
            ]

            f = open('ninupdates.xml', 'r')
            ninupdates = self.parse_feed(raw_bytes, f.read())
            for entry in ninupdates['new']['entries']:
                system, ver = entry['title'].split()
                if system not in consoles:
                    continue
                for entryold in ninupdates['old']['entries']:
                    systemold, verold = entryold['title'].split()
                    if systemold not in consoles:
                        continue
                    elif system == systemold and ver != verold:
                        channel = self.bot.get_channel(settings.NINUPDATE)
                        await channel.send(embed=discord.Embed(description=cleandoc('ℹ️ New update version for {}: [{}]({})'.format(system, ver, entry['link']))))
                        continue
            f.close()
            f = open('ninupdates.xml', 'wb')
            f.write(raw_bytes)
        f.close()

    async def subreddit(self):
        async with self.bot.session.get('https://www.reddit.com/r/ndsbrew/.rss') as resp:
            raw_bytes = await resp.read()
        if not os.path.isfile('ndsbrew.xml'):
            new = open('ndsbrew.xml', 'wb')
            new.write(raw_bytes)
            new.close()
        f = open('ndsbrew.xml', 'rb')
        if not self.digest_check(raw_bytes, f.read()):
            f.close()
            f = open('ndsbrew.xml', 'r', encoding='utf-8')
            ndsbrew = self.parse_feed(raw_bytes, f.read())
            last_updated = ndsbrew['new']['entries'][0]['updated_parsed']
            last_updated_old = ndsbrew['old']['entries'][0]['updated_parsed']
            if last_updated > last_updated_old:
                f.close()
                channel = self.bot.get_channel(settings.SUBREDDIT)

                embed = discord.Embed(colour=15549999)
                embed.title = ndsbrew['new']['entries'][0]['title']
                embed.url = ndsbrew['new']['entries'][0]['link']
                embed.set_author(name=ndsbrew['new']['entries'][0]['author_detail']['name'], url=ndsbrew['new']['entries'][0]['author_detail']['href'])
                embed.description = BeautifulSoup(ndsbrew['new']['entries'][0]['summary'], "html.parser").div.get_text()
                embed.set_footer(text=f"{ndsbrew['new']['feed']['tags'][0]['label']} • UTC {asctime(last_updated)}", icon_url=ndsbrew['new']['feed']['icon'][:-1])
                await channel.send(embed=embed)
                f = open('ndsbrew.xml', 'wb')
                f.write(raw_bytes)
        f.close()


def setup(bot):
    bot.add_cog(RSS(bot))

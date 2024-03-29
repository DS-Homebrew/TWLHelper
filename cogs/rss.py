#
# Copyright (C) 2021-2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#

import datetime
import functools
import logging
import os
from hashlib import sha256
from inspect import cleandoc
from time import mktime

import discord
import feedparser
from discord.ext import tasks, commands
from markdownify import markdownify


log = logging.getLogger("bot")


class RSS(commands.Cog):
    """RSS feeds"""

    def __init__(self, bot):
        self.bot = bot
        self.loop.start()

    @tasks.loop(minutes=10)
    async def loop(self):
        await self.bot.wait_until_ready()
        if self.bot.settings['NINUPDATE']:
            await self.ninupdates()
        if self.bot.settings['SUBREDDIT']:
            await self.subreddit()

    def digest_check(self, new, old):
        digestprev = sha256(old).digest()
        digestnext = sha256(new).digest()
        return digestprev == digestnext

    def parseFeed(self, new, old):
        feed = {}
        feed['new'] = feedparser.parse(new)
        feed['old'] = feedparser.parse(old)
        return feed

    async def asyncParseFeed(self, new, old):
        argv = functools.partial(self.parseFeed, new, old)
        return await self.bot.loop.run_in_executor(None, argv)

    async def getFeed(self, url: str, xml: str):
        async with self.bot.session.get(url) as resp:
            raw_bytes = await resp.read() if resp.status == 200 else None
        if not raw_bytes:
            log.info(f"{url} returned {resp.status}, skipping")
            return None
        if not os.path.isfile(xml):
            log.info(f"{url} polled for first time, will not send to channel")
            with open(xml, 'wb') as new:
                new.write(raw_bytes)
                return None
        with open(xml, 'rb') as f:
            if self.digest_check(raw_bytes, f.read()):
                log.info(f"{url} has no new content, skipping")
                return None
        with open(xml, 'r', encoding='utf-8') as f:
            feed = await self.asyncParseFeed(raw_bytes, f.read())
        with open(xml, 'wb') as f:
            f.write(raw_bytes)
        return feed

    async def ninupdates(self):
        ninupdates = await self.getFeed('https://yls8.mtheall.com/ninupdates/feed.php', 'data/ninupdates.xml')
        if not ninupdates:
            return

        consoles = [
            'Old3DS',
            'New3DS'
        ]
        for entry in ninupdates['new']['entries']:
            system, ver = entry['title'].split()
            if system not in consoles:
                continue
            for entryold in ninupdates['old']['entries']:
                systemold, verold = entryold['title'].split()
                if systemold not in consoles:
                    continue
                elif system == systemold and ver != verold:
                    channel = self.bot.get_channel(self.bot.settings['NINUPDATE'])
                    await channel.send(embed=discord.Embed(description=f"ℹ️ New update version for {system}: [{ver}]({entry['link']})"))
                    continue

    async def subredditEmbed(self, rss, idx):
        channel = self.bot.get_channel(self.bot.settings['SUBREDDIT'])
        entry = rss['entries'][idx]
        embed = discord.Embed(colour=15549999, timestamp=datetime.datetime.fromtimestamp(mktime(entry['updated_parsed'])))
        embed.title = entry['title']
        embed.url = entry['link']
        embed.set_author(name=entry['author_detail']['name'], url=entry['author_detail']['href'])
        embed.description = cleandoc(markdownify(entry['summary']))
        if len(embed.description) > 2000:
            embed.description = embed.description[:2000]
            embed.description += "\n..."
        embed.set_footer(text=f"{rss['feed']['tags'][0]['label']}", icon_url=rss['feed']['icon'][:-1])
        return await channel.send(embed=embed)

    async def subreddit(self):
        ndsbrew = await self.getFeed('https://www.reddit.com/r/ndsbrew/.rss', 'data/ndsbrew.xml')
        if not ndsbrew:
            return

        new_posts = []
        for idx, val in enumerate(ndsbrew['new']['entries']):
            if val not in ndsbrew['old']['entries']:
                new_posts.insert(0, idx)
        for idx in new_posts:
            await self.subredditEmbed(ndsbrew['new'], idx)


async def setup(bot):
    await bot.add_cog(RSS(bot))

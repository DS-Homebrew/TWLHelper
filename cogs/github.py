#
# Copyright (C) 2021-2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
import yarl
from discord.ext import commands

if TYPE_CHECKING:
    from ..twlhelper import TWLHelper


class GitHub(commands.Cog):
    """GitHub Webhook distribution"""

    def __init__(self, bot):
        self.bot: TWLHelper = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None:
            return

        if message.guild.id != self.bot.settings['GUILD']:
            return

        if message.channel.id == self.bot.settings['GITHUBUPDATES'] and message.embeds is not None:
            giturl = yarl.URL(message.embeds[0].url).path if message.embeds[0].url else ""
            if "DS-Homebrew/ChroniclesDX" in giturl or "[DS-Homebrew/ChroniclesDX]" in message.embeds[0].title:
                if self.bot.settings['DXUPDATES'] is not None:
                    thread = message.guild.get_thread(self.bot.settings['DXUPDATES'])
                    await thread.send(embeds=message.embeds)


async def setup(bot):
    await bot.add_cog(GitHub(bot))

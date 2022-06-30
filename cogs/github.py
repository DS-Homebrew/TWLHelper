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

    webupdate_list = [
        "DS-Homebrew/wiki",
        "cfw-guide/dsi.cfw.guide",
        "DS-Homebrew/twlmenu-extras",
        "DS-Homebrew/flashcard-archive"
    ]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None:
            return

        if message.guild.id != self.bot.settings['GUILD']:
            return

        if message.channel.id == self.bot.settings['GITHUBUPDATES'] and message.embeds is not None:
            giturl = yarl.URL(message.embeds[0].url).path
            if "DS-Homebrew/TWiLightMenu" in giturl or "[DS-Homebrew/TWiLightMenu]" in message.embeds[0].title:
                if self.bot.settings['TWLUPDATES'] is not None:
                    thread = message.guild.get_thread(self.bot.settings['TWLUPDATES'])
                    await thread.send(embeds=message.embeds)
            elif "DS-Homebrew/nds-bootstrap" in giturl or "[DS-Homebrew/nds-bootstrap]" in message.embeds[0].title:
                if self.bot.settings['NDSBUPDATES'] is not None:
                    thread = message.guild.get_thread(self.bot.settings['NDSBUPDATES'])
                    await thread.send(embeds=message.embeds)
            elif any(update in giturl for update in self.webupdate_list) or any(f"[{update}]" in message.embeds[0].title for update in self.webupdate_list):
                if self.bot.settings['WEBUPDATES'] is not None:
                    thread = message.guild.get_thread(self.bot.settings['WEBUPDATES'])
                    await thread.send(embeds=message.embeds)
            elif "DS-Homebrew/ChroniclesDX" in giturl or "[DS-Homebrew/ChroniclesDX]" in message.embeds[0].title:
                if self.bot.settings['DXUPDATES'] is not None:
                    thread = message.guild.get_thread(self.bot.settings['DXUPDATES'])
                    await thread.send(embeds=message.embeds)
            elif self.bot.settings['MISCUPDATES'] is not None:
                thread = message.guild.get_thread(self.bot.settings['MISCUPDATES'])
                await thread.send(embeds=message.embeds)


async def setup(bot):
    await bot.add_cog(GitHub(bot))

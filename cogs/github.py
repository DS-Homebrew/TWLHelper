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
import settings
import yarl


from discord.ext import commands


class GitHub(commands.Cog):
    """GitHub Webhook distribution"""

    def __init__(self, bot):
        self.bot = bot

    def guild_set():
        def predicate(ctx):
            if settings.GUILD is None:
                return False
            return True
        return commands.check(predicate)

    webupdate_list = [
        "DS-Homebrew/wiki",
        "cfw-guide/dsi.cfw.guide",
        "DS-Homebrew/twlmenu-extras",
        "DS-Homebrew/flashcard-archive"
    ]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == settings.GITHUBUPDATES and message.embeds is not None:
            giturl = yarl.URL(message.embeds[0].url).path
            if "DS-Homebrew/TWiLightMenu" in giturl or "[DS-Homebrew/TWiLightMenu]" in message.embeds[0].title:
                if settings.TWLUPDATES is not None:
                    thread = message.guild.get_thread(settings.TWLUPDATES)
                    await thread.send(embeds=message.embeds)
            elif "DS-Homebrew/nds-bootstrap" in giturl or "[DS-Homebrew/nds-bootstrap]" in message.embeds[0].title:
                if settings.NDSBUPDATES is not None:
                    thread = message.guild.get_thread(settings.NDSBUPDATES)
                    await thread.send(embeds=message.embeds)
            elif any(update in giturl for update in self.webupdate_list) or any(f"[{update}]" in message.embeds[0].title for update in self.webupdate_list):
                if settings.WEBUPDATES is not None:
                    thread = message.guild.get_thread(settings.WEBUPDATES)
                    await thread.send(embeds=message.embeds)
            else:
                if settings.MISCUPDATES is not None:
                    thread = message.guild.get_thread(settings.MISCUPDATES)
                    await thread.send(embeds=message.embeds)


async def setup(bot):
    await bot.add_cog(GitHub(bot))

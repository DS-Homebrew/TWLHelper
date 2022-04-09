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


from discord.ext import commands
from urllib.parse import quote


class International(commands.Cog):
    """International channel handling"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild.id == settings.GUILD:
            for i11l_channel in settings.I11L:
                if i11l_channel["ID"] == message.channel.id:
                    webhook = discord.Webhook.partial(
                        i11l_channel["WEBHOOK_ID"],
                        i11l_channel["WEBHOOK_TOKEN"],
                        session=self.bot.session
                    )

                    # Translate with DeepL
                    async with self.bot.session.get(f"https://api-free.deepl.com/v2/translate?auth_key={settings.DEEPLTOKEN}&target_lang=EN-US&text={quote(message.content)}") as response:
                        await webhook.send(
                            content=(await response.json())["translations"][0]["text"],
                            username=message.author.display_name,
                            avatar_url=message.author.avatar
                        )


async def setup(bot):
    await bot.add_cog(International(bot))

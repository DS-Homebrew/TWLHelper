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
from re import findall
from urllib.parse import quote


class International(commands.Cog):
    """International channel handling"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild.id == settings.GUILD and not message.webhook_id:
            for i11l_channel in settings.I11L:
                if i11l_channel["I11L"]["ID"] == message.channel.id:
                    webhook = discord.Webhook.partial(
                        i11l_channel["EN"]["WEBHOOK_ID"],
                        i11l_channel["EN"]["WEBHOOK_TOKEN"],
                        session=self.bot.session
                    )

                    # Translate with DeepL
                    async with self.bot.session.get(f"https://api-free.deepl.com/v2/translate?auth_key={settings.DEEPLTOKEN}&target_lang=EN-US&text={quote(message.content)}") as response:
                        translation = (await response.json())["translations"][0]
                        await webhook.send(
                            content=translation["text"],
                            username=f"{message.author.display_name} [{translation['detected_source_language']}]",
                            avatar_url=message.author.avatar
                        )
                elif i11l_channel["EN"]["ID"] == message.channel.id:
                    webhook = discord.Webhook.partial(
                        i11l_channel["I11L"]["WEBHOOK_ID"],
                        i11l_channel["I11L"]["WEBHOOK_TOKEN"],
                        session=self.bot.session
                    )

                    # Check for language code in name from autotranslated message
                    language_code = "EN"
                    if message.reference:
                        reply = await message.channel.fetch_message(message.reference.message_id)
                        matches = findall(r"\[([A-Z\-]{2,5})\]", reply.author.display_name)
                        if len(matches) > 0:
                            language_code = matches[0]

                    # If the message we're replying to isn't english, translate with DeepL
                    msg = message.content
                    if language_code != "EN":
                        async with self.bot.session.get(f"https://api-free.deepl.com/v2/translate?auth_key={settings.DEEPLTOKEN}&target_lang={language_code}&text={quote(msg)}") as response:
                            msg = (await response.json())["translations"][0]["text"]

                    await webhook.send(
                        content=msg,
                        username=message.author.display_name,
                        avatar_url=message.author.avatar
                    )


async def setup(bot):
    await bot.add_cog(International(bot))

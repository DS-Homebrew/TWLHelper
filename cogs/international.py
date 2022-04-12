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
import re
import settings


from datetime import datetime, timezone
from discord.ext import commands, tasks
from urllib.parse import quote


class International(commands.Cog):
    """International channel handling"""

    def __init__(self, bot):
        self.bot = bot
        self.VALID_LANGUAGE_CODES = [
            "BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "EN", "ES", "ET",
            "FI", "FR", "HU", "IT", "JA", "LT", "LV", "NL", "PL", "PT-PT",
            "PT-BR", "PT", "RO", "RU", "SK", "SL", "SV", "ZH"
        ]
        self.webhooks = {}
        for i11l_channel in settings.I11L:
            for item in i11l_channel:
                self.webhooks[i11l_channel[item]["ID"]] = discord.Webhook.partial(
                    i11l_channel[item]["WEBHOOK_ID"],
                    i11l_channel[item]["WEBHOOK_TOKEN"],
                    session=self.bot.session
                )
        self.messagecache = {}
        self.cleanup.start()

    @tasks.loop(minutes=10)
    async def cleanup(self):
        await self.bot.wait_until_ready()
        for id, message in dict(self.messagecache).items():
            if (datetime.now(timezone.utc) - message.created_at).seconds > 10 * 60:
                del self.messagecache[id]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message, edit=False):
        if message.guild.id == settings.GUILD and not message.webhook_id:
            for i11l_channel in settings.I11L:
                if i11l_channel["I11L"]["ID"] == message.channel.id:
                    # Translate with DeepL
                    async with self.bot.session.get(f"https://api-free.deepl.com/v2/translate?auth_key={settings.DEEPLTOKEN}&target_lang=EN-US&text={quote(message.content)}") as response:
                        translation = (await response.json())["translations"][0]
                        if edit:
                            await self.messagecache[message.id].edit(translation["text"])
                        else:
                            embed = None
                            if message.reference:
                                if message.reference.message_id in self.messagecache:
                                    reply = self.messagecache[message.reference.message_id]
                                else:
                                    id = next((id for id in self.messagecache if self.messagecache[id].id == message.reference.message_id), None)
                                    if id:
                                        ch = await message.guild.fetch_channel(i11l_channel["EN"]["ID"])
                                        reply = await ch.fetch_message(id)
                                    else:
                                        reply = await message.channel.fetch_message(message.reference.message_id)
                                embed = discord.Embed(description=reply.content)

                            webhookmsg = await self.webhooks[i11l_channel["EN"]["ID"]].send(
                                content=translation["text"],
                                username=f"{message.author.display_name} [{translation['detected_source_language']}]",
                                avatar_url=message.author.display_avatar,
                                embed=embed,
                                wait=True
                            )

                            self.messagecache[message.id] = webhookmsg
                    break
                elif i11l_channel["EN"]["ID"] == message.channel.id:
                    msg = message.content

                    language_code = "EN"
                    matches = re.findall(f"^({'|'.join(self.VALID_LANGUAGE_CODES)}):", msg, re.IGNORECASE)
                    if len(matches) > 0:
                        # Check if message specifies a language
                        language_code = matches[0].upper()
                        msg = msg[len(matches[0]) + 1:]
                    elif message.reference:
                        # Check for language code in name from autotranslated message
                        reply = await message.channel.fetch_message(message.reference.message_id)
                        matches = re.findall(r"\[([A-Z\-]{2,5})\]", reply.author.display_name)
                        if len(matches) > 0:
                            language_code = matches[0]

                    # If the message we're replying to isn't english, translate with DeepL
                    if language_code != "EN":
                        async with self.bot.session.get(f"https://api-free.deepl.com/v2/translate?auth_key={settings.DEEPLTOKEN}&target_lang={language_code}&text={quote(msg)}") as response:
                            msg = (await response.json())["translations"][0]["text"]

                    if edit:
                        await self.messagecache[message.id].edit(msg)
                    else:
                        embed = None
                        if message.reference:
                            if message.reference.message_id in self.messagecache:
                                reply = self.messagecache[message.reference.message_id]
                            else:
                                id = next((id for id in self.messagecache if self.messagecache[id].id == message.reference.message_id), None)
                                if id:
                                    ch = await message.guild.fetch_channel(i11l_channel["I11L"]["ID"])
                                    reply = await ch.fetch_message(id)
                                else:
                                    reply = await message.channel.fetch_message(message.reference.message_id)
                            embed = discord.Embed(description=reply.content)

                        webhookmsg = await self.webhooks[i11l_channel["I11L"]["ID"]].send(
                            content=msg,
                            username=message.author.display_name,
                            avatar_url=message.author.display_avatar,
                            embed=embed,
                            wait=True
                        )
                        self.messagecache[message.id] = webhookmsg
                    break

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.id in self.messagecache:
            await self.on_message(after, True)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.id in self.messagecache:
            await self.messagecache[message.id].delete()
            del self.messagecache[message.id]


async def setup(bot):
    await bot.add_cog(International(bot))

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

from typing import TYPE_CHECKING, Any, Optional, Sequence

import discord
from discord.ext import commands

from utils.utils import create_error_embed

if TYPE_CHECKING:
    from ..twlhelper import TWLHelper

__all__ = ("CustomView", "ViewPages")


class CustomView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        self.ctx: commands.Context[TWLHelper] = ctx
        self.message: Optional[discord.Message] = None
        super().__init__(timeout=60)

    async def on_error(self, interaction: discord.Interaction, exc: Any, item: discord.ui.Item):
        exc = getattr(exc, 'original', exc)
        if isinstance(exc, discord.Forbidden):
            await interaction.channel.send_message(f"💢 I can't help you if you don't let me!\n`{exc.text}`.")
        else:
            embed = create_error_embed(exc, interaction=interaction)
            await interaction.channel.send(f'{interaction.user.mention} Unexpected exception occurred', embed=embed)

    async def on_timeout(self):
        self.clear_items()
        await self.message.edit(view=self)
        self.stop()


# I would support other stuff than just embeds but this fine for now...
class ViewPages(CustomView):
    def __init__(self, source: Sequence[Any], ctx: commands.Context):
        self.current_page = 0
        self._source = source
        super().__init__(ctx)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This view is not for you!", ephemeral=True)
            return False
        return True

    async def format_page(self, entry: Any) -> discord.Embed:
        """A coroutine that allows you to format an entry.

        Subclasses should override this method to format an embed to be sent.

        Parameters
        ----------
        entry : Any
            A singular entry that was passed to source parameter.

        Returns
        -------
        discord.Embed
            An embed that's ready to be sent

        Raises
        ------
        NotImplementedError
            The subclass did not override this method.
        """
        raise NotImplementedError

    async def start(self, *, destination: Optional[discord.abc.Messageable] = None):
        """Starts the pagination menu

        Parameters
        ----------
        destination : discord.abc.Messageable, optional
            An optional destination channel to send the menu to, by default None
        """
        kwargs = {'embed': await self.get_page(), 'view': self}
        if destination:
            self.message = await destination.send(**kwargs)
        else:
            self.message = await self.ctx.send(**kwargs)

    async def get_page(self):
        page = self.source[self.current_page]
        return await self.format_page(page)

    def get_max_pages(self):
        return len(self.source) - 1

    @property
    def source(self):
        return self._source

    @discord.ui.button(label='Previous')
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page == 0:
            await interaction.response.edit_message(embed=await self.get_page())
            return

        self.current_page -= 1
        await interaction.response.edit_message(embed=await self.get_page())

    @discord.ui.button(label='Next')
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page == self.get_max_pages():
            await interaction.response.edit_message(embed=await self.get_page())
            return

        self.current_page += 1
        await interaction.response.edit_message(embed=await self.get_page())

    @discord.ui.button(label='Close', style=discord.ButtonStyle.red)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        self.stop()

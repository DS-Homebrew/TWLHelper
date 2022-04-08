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
import json
from typing import Any, Optional, Sequence

import discord
from discord.ext import commands
from rapidfuzz import process

from utils.utils import create_error_embed

__all__ = ("CustomView", "ViewPages")


class CustomView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    message: discord.Message = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.ctx.author == interaction.user

    async def on_error(self, exc: Any, item: discord.ui.Item, interaction: discord.Interaction):
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
        self.ctx = ctx
        self.current_page = 0
        self._source = source
        super().__init__()

    async def format_initial_message(self):
        return await self.get_page()

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
            An embed

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
        kwargs = {'embed': await self.format_initial_message(), 'view': self}
        if destination:
            await destination.send(**kwargs)
        else:
            await self.ctx.send(**kwargs)

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


class NBCompatView(CustomView):
    def __init__(self, ctx, argument, israndom=False):
        self.title = argument
        self.ctx = ctx
        self.bot = ctx.bot
        self.iterator = 0
        self.iteratorcap = 0
        super().__init__()

    games = []
    compatlist = None

    def getGameValues(self, name, compatlist):
        for line in compatlist:
            if name == line[1]:
                return line
        return None

    def nbembed(self, game, compatlist):
        embed = discord.Embed()
        embed.title = f"{game[1]} ({game[4]})"
        embed.add_field(name="Last tested version", value=f"{game[10]}", inline=False)
        embed.add_field(name="Compatibility", value=f"{game[13]}", inline=False)
        if game[14] != '':
            embed.add_field(name="Notes", value=f"{game[14]}", inline=False)
        gameidx = self.search_tid(game[3], compatlist, getlink=True)
        embed.add_field(name="Link", value=f"https://docs.google.com/spreadsheets/d/1LRTkXOUXraTMjg1eedz_f7b5jiuyMv2x6e_jY_nyHSc/edit#gid=0&range=A{gameidx}:P{gameidx}", inline=False)
        return embed

    # This function is based on UDB-API, licensed Apache-2.0.
    # https://github.com/LightSage/UDB-API
    def search_name(self, arg, compatlist):
        matchlist = []
        game_names = [line[1] for line in compatlist[2:]]
        results = process.extract(arg, [g.lower() for g in game_names], processor=lambda a: a.lower())
        for _, score, idx in results:
            if score < 70:
                continue
            game = self.getGameValues(game_names[idx], compatlist)
            matchlist.append(game)
        return matchlist

    def search_tid(self, arg, compatlist, getlink=False):
        matchlist = []
        for idx, val in enumerate(compatlist[2:]):
            if arg.upper() in val[3]:
                if getlink:
                    # +1 because sheet starts from 1, but list starts from 0
                    # +2 added since searching starts from row 3
                    return idx + 3
                matchlist.append(val)
                return matchlist
        return None

    async def start(self):
        game = None
        tid = len(self.title) == 4
        if tid and self.title[0] in ['H', 'Z', 'K']:
            await self.ctx.send("DSiWare compatibility is not supported. Please try another game, or visit the list directly.")
            return self.stop()
        with open("nbcompat.json", "r") as compatfile:
            self.compatlist = json.load(compatfile)
        if tid:
            game = self.search_tid(self.title, self.compatlist, getlink=False)
        if not game:
            tid = False
            game = self.search_name(self.title, self.compatlist)
        if game:
            view = None if tid else self
            self.games = game
            self.iteratorcap = len(self.games) - 1
            self.message = await self.ctx.send(embed=self.nbembed(self.games[0], self.compatlist), view=view)
            return
        with open("nbcompat-fallback.json") as compatfile:
            self.compatlist = json.load(compatfile)
        if tid:
            game = self.search_tid(self.title, self.compatlist, getlink=False)
        else:
            game = self.search_name(self.title, self.compatlist)
        if game:
            return await self.ctx.send(f"{game[0][1]} ({game[0][4]}) does not have any compatibility ratings!")
        await self.ctx.send("Game not found. Please try again.")

    @discord.ui.button(label='Previous')
    async def previousbutton(self, interaction: discord.Interaction, button):
        if self.iterator == 0:
            return await interaction.response.defer()
        self.iterator -= 1
        await interaction.response.edit_message(embed=self.nbembed(self.games[self.iterator], self.compatlist))

    @discord.ui.button(label='Next')
    async def nextbutton(self, interaction: discord.Interaction, button):
        if self.iterator == self.iteratorcap:
            return await interaction.response.defer()
        self.iterator += 1
        await interaction.response.edit_message(embed=self.nbembed(self.games[self.iterator], self.compatlist))

    @discord.ui.button(label='Close')
    async def closebutton(self, interaction: discord.Interaction, button):
        self.clear_items()
        await interaction.response.edit_message(embed=self.nbembed(self.games[self.iterator], self.compatlist), view=self)
        self.stop()

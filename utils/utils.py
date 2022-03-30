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


import traceback
import discord
import settings

from typing import Any, Optional
from discord.ext import commands

__all__ = ("create_error_embed",
           "is_staff",
           "check_arg",
           "web_name")


def create_error_embed(exc: Any, ctx: Optional[commands.Context] = None, interaction: Optional[discord.Interaction] = None) -> discord.Embed:
    trace = "".join(traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__, chain=False))
    embed = discord.Embed(title="Unexpected exception", description=f"```py\n{trace}```", color=0xe50730)

    if ctx:
        embed.title += f" in command {ctx.command}"
        channelfmt = ctx.channel.mention if ctx.guild else "Direct Message"
        embed.add_field(name="Channel", value=channelfmt)
        embed.add_field(name="Invocation", value=ctx.message.content)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
    elif interaction:
        embed.title += " in interaction"
        channelfmt = interaction.channel.mention if interaction.guild else "Direct Message"
        embed.add_field(name="Channel", value=channelfmt)
        if interaction.message.content:
            embed.add_field(name="Invocation", value=interaction.message.content)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)

    embed.add_field(name="Exception Type", value=exc.__class__.__name__)
    return embed


def is_staff():
    def predicate(ctx):
        return any((role.id in settings.staff_roles or role.name in settings.staff_roles) for role in ctx.message.author.roles) if not ctx.author == ctx.guild.owner else True
    return commands.check(predicate)


def check_arg(argument: str, arg) -> bool:
    """Helper util to check if an argument is in a sequence.

    Returns a boolean indicator if the argument was found in the supplied sequence"""
    if argument.lower() in arg:
        return True
    return False


def web_name(name):
    name = name.lower()
    out = ""
    for letter in name:
        if letter in "abcdefghijklmnopqrstuvwxyz0123456789-_":
            out += letter
        elif letter in ". ":
            out += "-"
    return out

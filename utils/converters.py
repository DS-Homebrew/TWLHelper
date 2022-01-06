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

from discord.ext import commands

__all__ = ("Literal",)


class Literal(commands.Converter):
    """Similar to typing.Literal except this is designed for lowercased literals.

    This also calls str.lower() on the argument during conversion.
    """
    def __init__(self, *literals):
        self.literals = [x.lower() for x in literals]

    async def convert(self, ctx: commands.Context, argument: str) -> str:
        largument = argument.lower()
        if largument in self.literals:
            return largument
        else:
            raise commands.BadArgument(f"Expected one of the following: {', '.join(self.literals)}.")

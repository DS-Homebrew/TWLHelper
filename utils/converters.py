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
            raise commands.UserInputError(f"Expected one of {' '.join(self.literals)}.")

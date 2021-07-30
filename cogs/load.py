#
# Copyright (C) 2020 Nintendo Homebrew
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from discord.ext import commands
from utils.utils import is_staff


class Load(commands.Cog):
    """
    Load commands.
    """
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        return True

    @is_staff()
    @commands.command()
    async def load(self, ctx, *, module: str):
        """Loads a Cog."""
        try:
            if module[0:7] != "cogs.":
                module = "cogs." + module
            self.bot.load_extension(module)
            await ctx.send('✅ Extension loaded.')
        except Exception as e:
            await ctx.send(f'💢 Failed!\n```\n{type(e).__name__}: {e}\n```')

    @is_staff()
    @commands.command()
    async def unload(self, ctx, *, module: str):
        """Unloads a Cog."""
        try:
            if module[0:7] != "cogs.":
                module = "cogs." + module
            if module == "cogs.load":
                await ctx.send("❌ I don't think you want to unload that!")
            else:
                self.bot.unload_extension(module)
                await ctx.send('✅ Extension unloaded.')
        except Exception as e:
            await ctx.send(f'💢 Failed!\n```\n{type(e).__name__}: {e}\n```')

    @is_staff()
    @commands.command(name='reload')
    async def reload(self, ctx, *, module: str):
        """Reloads a Cog."""
        try:
            if module[0:7] != "cogs.":
                module = "cogs." + module
            self.bot.reload_extension(module)
            await ctx.send('✅ Extension reloaded.')
        except Exception as e:
            await ctx.send(f'💢 Failed!\n```\n{type(e).__name__}: {e}\n```')


def setup(bot):
    bot.add_cog(Load(bot))

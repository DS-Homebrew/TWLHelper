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


import discord
import json

from discord.ext import commands

settingsf = open('settings.json')
settings = json.load(settingsf)


async def send_dm_message(member: discord.Member, message: str, ctx: commands.Context = None, **kwargs) -> bool:
    """A helper method for sending a message to a member's DMs.

    Returns a boolean indicating success of the DM
    and notifies of the failure if ctx is supplied."""
    try:
        await member.send(message, **kwargs)
        return True
    except (discord.HTTPException, discord.Forbidden, discord.NotFound, AttributeError):
        if ctx:
            await ctx.send(f"Failed to send DM message to {member.mention}")
        return False


def command_signature(command, *, prefix=".") -> str:
    """Helper method for a command signature

    Parameters
    -----------
    command: :class:`discord.ext.commands.Command`
        The command to generate a signature for
    prefix: str
        The prefix to include in the signature"""
    signature = f"{discord.utils.escape_markdown(prefix)}{command.qualified_name} {command.signature}"
    return signature


def create_error_embed(ctx, exc) -> discord.Embed:
    embed = discord.Embed(title=f"Unexpected exception in command {ctx.command}", color=0x2F3136)
    embed.add_field(name=f"{exc.__class__.__name__} Exception ", value=exc, inline=False)
    embed.add_field(name="Information", value=f"channel: {ctx.channel.mention if isinstance(ctx.channel, discord.TextChannel) else 'Direct Message'}\ncommand: {ctx.command}\nmessage: {ctx.message.content}\nuser: {ctx.author.mention}", inline=False)
    return embed


def is_staff():
    def predicate(ctx):
        return any(ctx.message.author.roles == role for role in settings['MODERATOR']) if not ctx.author == ctx.guild.owner else True
    return commands.check(predicate)

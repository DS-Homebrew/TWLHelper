#
# Copyright (C) 2017-2022 Nintendo Homebrew
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
#
# netinfo from loop.py

import discord

from datetime import datetime
from pytz import timezone
from discord.ext import commands, tasks


class NetInfo(commands.Cog):
    """
    Nintendo Network status information
    """

    def __init__(self, bot):
        self.bot = bot
        self.loop.start()

    @tasks.loop(seconds=1800)
    async def loop(self):
        await self.bot.wait_until_ready()
        await self.update_netinfo()

    netinfo_embed = discord.Embed(description="The Network Maintenance Information page has not been successfully checked yet.")

    def netinfo_parse_time(self, timestr):
        # netinfo is US/Pacific. Convert it to UTC so Discord timestamp works
        return timezone('US/Pacific').localize(datetime.strptime(' '.join(timestr.split()), '%A, %B %d, %Y %I :%M %p')).astimezone(timezone('UTC'))

    async def update_netinfo(self):
        async with self.bot.session.get('https://www.nintendo.co.jp/netinfo/en_US/status.json?callback=getJSON', timeout=45) as r:
            if r.status == 200:
                j = await r.json()
            else:
                self.netinfo_embed.description = "Failure when checking the Network Maintenance Information page."
                return

        now = datetime.now(timezone('US/Pacific'))

        embed = discord.Embed(title="Network Maintenance Information / Online Status",
                              url="https://www.nintendo.co.jp/netinfo/en_US/index.html",
                              timestamp=now)
        embed.set_footer(text="This information was last updated:")

        for status_type in ("operational_statuses", "temporary_maintenances"):
            descriptor = "Maintenance" if status_type == "temporary_maintenances" else "Status"

            for entry in j[status_type]:
                if "platform" in entry:
                    entry_desc = ', '.join(entry["platform"]).replace("nintendo", "Nintendo").replace("web", "Web")
                else:
                    entry_desc = 'No console specified.'

                begin = datetime(year=2000, month=1, day=1, tzinfo=timezone('US/Pacific'))
                end = datetime(year=2099, month=1, day=1, tzinfo=timezone('US/Pacific'))
                if "begin" in entry:
                    begin = self.netinfo_parse_time(entry["begin"])
                    entry_desc += '\nBegins: ' + discord.utils.format_dt(begin, style='F')
                if "end" in entry:
                    end = self.netinfo_parse_time(entry["end"])
                    entry_desc += '\nEnds: ' + discord.utils.format_dt(end, style='F')

                if now < end:
                    entry_name = "{} {}: {}".format(
                        "Current" if begin <= now else "Upcoming",
                        descriptor,
                        entry["software_title"].replace(' <br />\r\n', ', ')
                    )
                    if "services" in entry:
                        entry_name += ", " + ', '.join(entry["services"])
                    embed.add_field(name=entry_name, value=entry_desc, inline=False)
        if len(embed.fields) == 0:
            embed.description = "No ongoing or upcoming maintenances."
        self.netinfo_embed = embed

    @commands.command()
    async def netinfo(self, ctx):
        """Shows the Nintendo Network status information"""
        await ctx.send(embed=self.netinfo_embed)


def setup(bot):
    bot.add_cog(NetInfo(bot))

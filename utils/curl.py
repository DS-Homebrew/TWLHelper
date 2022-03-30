import json
import discord

from discord import Interaction
from rapidfuzz import process
from utils.utils import web_name, create_error_embed


class CustomView(discord.ui.View):
    async def on_error(self, exc, item: discord.ui.Item, interaction: Interaction, ):
        author: discord.Member = interaction.user
        exc = getattr(exc, 'original', exc)
        channel = interaction.channel

        if isinstance(exc, discord.NotFound):
            await channel.send("ID not found.")

        elif isinstance(exc, discord.Forbidden):
            await channel.send(f"💢 I can't help you if you don't let me!\n`{exc.text}`.")

        else:
            await channel.send(f'{author.mention} Unexpected exception occurred')
            embed = create_error_embed(exc)
            await channel.send(embed=embed)


class UniStoreView(CustomView):
    def __init__(self, ctx, argument, store, israndom=False):
        self.argument = argument
        self.ctx = ctx
        self.bot = ctx.bot
        self.store = store
        self.israndom = israndom
        self.iterator = 0
        self.iteratorcap = 0
        super().__init__()

    apps = {}

    def unistoreapp(self, appid, store):
        embed = discord.Embed()
        embed.title = appid["title"]
        embed.color = int(appid['color'][1:], 16) if 'color' in appid else None
        embed.set_author(name=appid["author"], icon_url=appid["avatar"] if "avatar" in appid else None)
        embed.set_thumbnail(url=appid["icon"] if "icon" in appid else (appid["image"] if "image" in appid else (appid["avatar"] if "avatar" in appid else None)))
        embed.description = appid["description"] if "description" in appid else None
        if store == "udb":
            embed.url = f'https://db.universal-team.net/{appid["systems"][0].lower()}/'
        else:
            embed.url = f'https://skins.ds-homebrew.com/{store}/'
        embed.url += web_name(appid["title"])
        return embed

    async def udbparse(self, ctx, search="", israndom=False):
        app = None
        r = None
        async with ctx.typing():
            if israndom or search != "":
                if israndom:
                    r = await self.bot.session.get("https://udb-api.lightsage.dev/random")
                elif search != "":
                    r = await self.bot.session.get(f"https://udb-api.lightsage.dev/search/{search}")
                if r.status == 200:
                    app = await r.json()
                elif r.status == 422:
                    await ctx.send("HTTP 422: Validation error. Please try again later.")
                    return self.stop()
                else:
                    await ctx.send("Unknown response from API. Please try again later.")
                    return self.stop()
            if israndom:
                await ctx.send(embed=self.unistoreapp(app[0], "udb"))
                return self.stop()
            elif search != "":
                if app["results"]:
                    self.apps = app["results"]
                    self.iteratorcap = len(self.apps) - 1
                    return await ctx.send(embed=self.unistoreapp(self.apps[0], "udb"), view=self)
                else:
                    await ctx.send("App cannot be found. Please try again.")
                    return self.stop()
            # when no args
            embed = discord.Embed(title="Universal-DB", colour=0x1d8056)
            embed.url = "https://db.universal-team.net/"
            embed.set_author(name="Universal-Team")
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/49733679?s=400&v=4")
            embed.description = "A database of DS and 3DS homebrew"
            await ctx.send(embed=embed)
            return self.stop()

    async def skinparse(self, ctx, skin="", israndom=False):
        item = None
        r = None
        async with ctx.typing():
            if skin != "" or israndom:
                if israndom:
                    r = await self.bot.session.get(f"https://twlmenu-extras.api.hansol.ca/random/{self.store}")
                elif skin != "":
                    r = await self.bot.session.get(f"https://twlmenu-extras.api.hansol.ca/search/{self.store}/{skin}")
                if r.status == 200:
                    item = await r.json()
                elif r.status == 422:
                    await ctx.send("HTTP 422: Validation error. Please try again later.")
                    return self.stop()
                else:
                    await ctx.send("Unknown response from API. Please try again later.")
                    return self.stop()
            if israndom:
                return await ctx.send(embed=self.unistoreapp(item[0], web_name(self.store)))
            elif skin != "":
                if item["results"]:
                    self.apps = item["results"]
                    self.iteratorcap = len(self.apps) - 1
                    self.store = web_name(self.store)
                    return await ctx.send(embed=self.unistoreapp(self.apps[0], self.store), view=self)
                else:
                    await ctx.send("Skin cannot be found. Please try again.")
                    return self.stop()
            # when no args
            embed = discord.Embed(colour=0xda4a53)
            embed.url = f"https://skins.ds-homebrew.com/{web_name(self.store)}/"
            embed.set_author(name="DS-Homebrew")
            if self.store == "Unlaunch":
                embed.title = "Unlaunch Backgrounds"
                embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
                embed.description = "Custom backgrounds for Unlaunch"
            elif self.store == "Nintendo DSi":
                embed.title = "DSi Menu Skins"
                embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/dsi.png")
                embed.description = "Custom skins for TWiLight Menu++'s DSi Menu theme"
            elif self.store == "R4 Original":
                embed.title = "R4 Original Menu Skins"
                embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/r4.png")
                embed.description = "Custom skins for TWiLight Menu++'s R4 Original Menu theme"
            elif self.store == "Nintendo 3DS":
                embed.title = "3DS Menu Skins"
                embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/3ds.png")
                embed.description = "Custom skins for TWiLight Menu++'s 3DS Menu theme"
            elif self.store == "Font":
                embed.title = "TWiLight Menu++ Fonts"
                embed.set_thumbnail(url="https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/unistore/icons/font.png")
                embed.description = "Custom fonts for TWiLight Menu++"
            elif self.store == "Icon":
                embed.title = "TWiLight Menu++ Icons"
                embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
                embed.description = "Custom icons for TWiLight Menu++"
            await ctx.send(embed=embed)
            return self.stop()

    async def start(self):
        if self.store == "udb":
            await self.udbparse(self.ctx, self.argument, israndom=self.israndom)
        else:
            await self.skinparse(self.ctx, skin=self.argument, israndom=self.israndom)

    @discord.ui.button(label='Previous')
    async def previousbutton(self, interaction: Interaction, button):
        if self.iterator == 0 or self.ctx.author != interaction.user:
            return await interaction.response.defer()
        self.iterator -= 1
        await interaction.response.edit_message(embed=self.unistoreapp(self.apps[self.iterator], self.store))

    @discord.ui.button(label='Next')
    async def nextbutton(self, interaction: Interaction, button):
        if self.iterator == self.iteratorcap or self.ctx.author != interaction.user:
            return await interaction.response.defer()
        self.iterator += 1
        await interaction.response.edit_message(embed=self.unistoreapp(self.apps[self.iterator], self.store))

    @discord.ui.button(label='Close')
    async def closebutton(self, interaction: Interaction, button):
        if self.ctx.author != interaction.user:
            return await interaction.response.defer()
        super().clear_items()
        await interaction.response.edit_message(embed=self.unistoreapp(self.apps[self.iterator], self.store), view=self)
        return self.stop()


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
                if not getlink:
                    matchlist.append(val)
                    return matchlist
                else:
                    # +1 because sheet starts from 1, but list starts from 0
                    # +2 added since searching starts from row 3
                    return idx + 3
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
        else:
            game = self.search_name(self.title, self.compatlist)
        if game:
            view = None if tid else self
            self.games = game
            self.iteratorcap = len(self.games) - 1
            return await self.ctx.send(embed=self.nbembed(self.games[0], self.compatlist), view=view)
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
    async def previousbutton(self, interaction: Interaction, button):
        if self.iterator == 0 or self.ctx.author != interaction.user:
            return await interaction.response.defer()
        self.iterator -= 1
        await interaction.response.edit_message(embed=self.nbembed(self.games[self.iterator], self.compatlist))

    @discord.ui.button(label='Next')
    async def nextbutton(self, interaction: Interaction, button):
        if self.iterator == self.iteratorcap or self.ctx.author != interaction.user:
            return await interaction.response.defer()
        self.iterator += 1
        await interaction.response.edit_message(embed=self.nbembed(self.games[self.iterator], self.compatlist))

    @discord.ui.button(label='Close')
    async def closebutton(self, interaction: Interaction, button):
        if self.ctx.author != interaction.user:
            return await interaction.response.defer()
        super().clear_items()
        await interaction.response.edit_message(embed=self.nbembed(self.games[self.iterator], self.compatlist), view=self)
        return self.stop()

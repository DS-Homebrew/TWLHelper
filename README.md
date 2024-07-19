# TWLHelper, DS⁽ⁱ⁾ Mode Hacking Discord server bot

## How to use

1. Make a copy of `settings.json.example` and name it `settings.json`.
1. Set your bot's token ID.
    - You will need to create a bot over at [Discord Developer Portal](https://discord.com/developers/applications).
1. You can also set other arguments in `settings.json`, such as command prefix, account status, and moderator roles.
    - It is recommended to use IDs rather than names for Moderator Roles to make sure jishaku can't be hijacked.
    - If none are set, all moderation permissions will default to either the guild owner or the bot owner.
1. Install the following for your host:
    - Python 3.10.x (and its respective pip)
1. Create a venv and activate it
    - UNIX-based: `python3 -m venv venv`, `source venv/bin/activate`
    - Windows `py -m venv venv`, `.\venv\Scripts\activate`
1. Run `pip install -r requirements.txt`
1. Run the following command:
    - UNIX-based: `python3 twlhelper.py`
    - Windows: `py twlhelper.py`

### Optional functions

Each function and related commands will be disabled until the instructions are followed correctly.

- The nds-boostrap compatibility list uses gspread, which requires a Google API key.
    1. You can read a guide on how to get this key here: https://docs.gspread.org/en/latest/oauth2.html
    1. In `settings.json`, set `GSPREADKEY` to the relative path of your API key JSON file.
- The Convert cog converts images, videos, and audio to a certain format, primarily designed for TWiLight Menu++ theming and video players.
    - To use the image/video/audio conversion functions, install `ffmpeg` for your host.
    - To use the Unlaunch background conversion functions, install `ffmpeg` and `gifsicle` for your host.
    - To use the GBARunner2 border conversion functions, install `grit` for your host. This can be found by installing the [devkitPro build environment](https://devkitpro.org/wiki/Getting_Started).
        - If your host is already configured to compile NDS or GBA software, this should already be set up.
        - If only installing the devkitPro build environment specifically for `grit`, you will need to install both `grit` and `devkit-env` package from pacman.
- The NoIntro cog has commands related to searching the No-Intro database.
    - For now, only Nintendo DS games are supported.
    - In `settings.json`, set `NOINTRO` to the relative path of the database file.
        - This is by default set to the pre-provided `no-intro.dat` file.

### Docker

TWLHelper is also provided as a Docker container.

How to use:
1. Download `docker-compose-prod.yml` to a self-contained folder of your choice, rename it to `docker-compose.yml`
1. Create a `data` folder (it should already exist if you previously cloned the repository)
1. If you use the nds-bootstrap compatibility list feature, copy the `GSPREADKEY` file to the `data` folder, then set your `settings.json` accordingly
1. Run `docker compose up -d`

## License
```
ISC License

Copyright (C) 2021-2022 DS-Homebrew

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

## Credits
- Discord.py: This wouldn't exist without it
- [Nintendo Homebrew's Kurisu](https://github.com/nh-server/kurisu): `assistance.py`, netinfo, simple_embed
    - Licensed under Apache 2.0. See source, or see http://www.apache.org/licenses/LICENSE-2.0.
- [YourKalamity](https://github.com/YourKalamity): `convert.py` code used with permission
- [LightSage's UDB-API](https://github.com/LightSage/UDB-API): fuzzy searching
    - Licensed under Apache 2.0. See source, or see http://www.apache.org/licenses/LICENSE-2.0.
- No-Intro: Nintendo DS database
    - All values were set to default when generating from the website.

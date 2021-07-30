# TWLHelper, DS⁽ⁱ⁾ Mode Hacking Discord server bot

## How to use

1. Make a copy of `settings.json.example` and name it `settings.json`.
1. Set your bot's token ID.
    - You will need to create a bot over at [Discord Developer Portal](https://discord.com/developers/applications).
1. You can also set other arguments in `settings.json`, such as command prefix, account status, and moderator roles.

There are currently two ways to run the bot:

### Docker:
1. Just run `docker-compose up --build -d`.

### Command line:
1. Install the latest version of Python 3, at minimum 3.8, for your host.
1. Install ImageMagick for your host. At this time, the code expects ImageMagick 6. Any other version is UNTESTED.
1. Install Gifsicle and ffmpeg for your host.
1. Run `pip install -r requirements.txt`.
1. Run the following command:
    - UNIX-based: `python3 twlhelper.py`
    - Windows: `py twlhelper.py`

## License

All files without a license in its header are licensed to the following:
```
ISC License

Copyright (C) 2021 DS-Homebrew

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
- [Nintendo Homebrew's Kurisu](https://github.com/nh-server/kurisu): `utils.py` error embeds, `load.py`, `assistance.py` simple_embed and console-specific identifiers
- [YourKalamity](https://github.com/YourKalamity): `convert.py` code used with permission

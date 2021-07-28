# DS⁽ⁱ⁾ Mode Hacking Discord server bot

## How to use

1. Make a copy of `settings.ini.example` and name it `settings.ini`.
1. Set your bot's token ID.
    - Do *not* use quotes. It can be inputted directly.
    - You will need to create a bot over at [Discord Developer Portal](https://discord.com/developers/applications).
1. You can also set other arguments in `settings.ini`, such as command prefix or account status.

There are currently two ways to run the bot:

### Docker:
1. Just run `docker-compose up --build -d`.
    - If you want to use the [discord.py master](https://github.com/Rapptz/discord.py) branch, run `docker-compose -f docker-compose-master.yml up --build -d`.
        - This is UNTESTED. Use at your own risk.

### Command line:
1. Install the latest version of Python 3, at minimum 3.8, for your host.
1. Run `pip install -r requirements.txt`.
    - If you want to use the [discord.py master](https://github.com/Rapptz/discord.py) branch, run `pip install -r requirements-master.txt`.
        - If you want to switch back to the release branch, you **must** re-run the regular `pip` command!
        - This is UNTESTED. Use at your own risk.
1. Run the following command:
    - UNIX-based: `python3 twlbot.py`
    - Windows: `py twlbot.py`

## License

All files without a license in its header are licensed to the following:
```
Copyright (C) 2021 DS-Homebrew

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

## Credits
- Discord.py: This wouldn't exist without it
- [Nintendo Homebrew's Kurisu](https://github.com/nh-server/kurisu): `utils.py` error embeds, `assistance.py` simple_embed and console-specific identifiers
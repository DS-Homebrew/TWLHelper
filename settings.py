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

import os
import json

IS_DOCKER = os.environ.get('IS_DOCKER', '')

# Load config
settingsf = open('settings.json')
settings = json.load(settingsf)

# bot internals
TOKEN = settings['DEFAULT']['TOKEN']
PREFIX = [x for x in settings['DEFAULT']['PREFIX']]
STATUS = settings['DEFAULT']['STATUS']
GSPREADKEY = settings.get('GSPREADKEY')

# server specifics
GUILD = settings.get('GUILD')
staff_roles = [x for x in settings['MODERATOR']]

# channels
NINUPDATE = settings['CHANNEL']['NINUPDATES']
SUBREDDIT = settings['CHANNEL']['SUBREDDIT']
GITHUBUPDATES = settings['CHANNEL']['GITHUBUPDATES']

# threads
TWLUPDATES = settings['THREAD']['TWLUPDATES']
NDSBUPDATES = settings['THREAD']['NDSBUPDATES']
WEBUPDATES = settings['THREAD']['WEBUPDATES']
MISCUPDATES = settings['THREAD']['MISCUPDATES']

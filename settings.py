#
# Copyright (C) 2021-2022 DS-Homebrew
#
# SPDX-License-Identifier: ISC
#

import json
from typing import Any, Dict


def loadSettings() -> Dict[str, Any]:
    # Load config
    with open("settings.json", "r") as f:
        settings = json.load(f)

    ret = {}
    # bot internals
    ret['TOKEN'] = settings['DEFAULT']['TOKEN']
    ret['PREFIX'] = [x for x in settings['DEFAULT']['PREFIX']]
    ret['STATUS'] = settings['DEFAULT']['STATUS']
    ret['GSPREADKEY'] = settings.get('GSPREADKEY')
    ret['NOINTRO'] = settings.get('NOINTRO')

    # server specifics
    ret['GUILD'] = settings.get('GUILD')
    ret['staff_roles'] = [x for x in settings['MODERATOR']]

    return ret

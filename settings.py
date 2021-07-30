import os
import json

IS_DOCKER = os.environ.get('IS_DOCKER', '')

# Load config
if IS_DOCKER:
    settingsf = open(os.environ.get('twlhelper_settings_json'))
    settings = json.load(settingsf)

else:
    settingsf = open('settings.json')
    settings = json.load(settingsf)


TOKEN = settings['DEFAULT']['TOKEN']
PREFIX = [x for x in settings['DEFAULT']['PREFIX']]
STATUS = settings['DEFAULT']['STATUS']
staff_roles = [x for x in settings['MODERATOR']]

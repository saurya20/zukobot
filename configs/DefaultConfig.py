import configparser

config =configparser.ConfigParser()
config.read('config.env')

DISCORD_OWNER_ID = config['DEFAULT']['discord_owner_id']
DISCORD_SDK = config['DEFAULT']['discord_sdk']
GEMINI_SDK = config['DEFAULT']['gemini_sdk']
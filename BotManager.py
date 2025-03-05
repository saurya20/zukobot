import configs.DefaultConfig as defaultConfig
import utils.DiscordUtil as discordUtil

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!",intents=intents,help_command=None)

@bot.event
async def on_ready():
    print("Bot is online..")

bot.run(defaultConfig.DISCORD_SDK)
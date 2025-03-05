import configs.DefaultConfig as defaultConfig
import utils.DiscordUtil as discordUtil
import asyncio
import discord
from discord.ext import commands
from cogs.GeminiCog import GeminiAgent
import re

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="#",intents=intents,help_command=None)


@bot.event
async def on_ready():
    print("Bot is online..")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")  
    if channel:
        await channel.send(f"Welcome {member.mention} to the server! 🎉 Feel free to introduce yourself.")

@bot.command(aliases = ["about"])
async def help(ctx):
    MyEmbed = discord.Embed(title = "Commands",
                            description = "These are the Commands that you can use for this bot.",
                            color = discord.Color.dark_purple())
    MyEmbed.set_thumbnail(url = "https://th.bing.com/th/id/OIG.UmTcTiD5tJbm7V26YTp.?w=270&h=270&c=6&r=0&o=5&pid=ImgGn")
    MyEmbed.add_field(name = "#query", value = "This command allows you to communicate with Gemini AI Bot on the Server. Please wrap your questions with quotation marks.", inline = False)
    MyEmbed.add_field(name="#remind YYYY-MM-DD HH:MM <message>", value="Set a reminder.", inline=False)
    MyEmbed.add_field(name="#listreminders", value="List all active reminders.", inline=False)
    MyEmbed.add_field(name="#deletereminder YYYY-MM-DD HH:MM", value="Delete a specific reminder.", inline=False)
    MyEmbed.set_footer(text="Use '#' before each command")
    await ctx.send(embed = MyEmbed)

@bot.command()
@commands.check(discordUtil.is_me)
async def unloadGemini(ctx):
    await bot.remove_cog('GeminiAgent')

@bot.command()
@commands.check(discordUtil.is_me)
async def reloadGemini(ctx):
    await bot.add_cog(GeminiAgent(bot))

async def startcogs():
    await bot.add_cog(GeminiAgent(bot))
    await bot.load_extension("cogs.RemindersCog")
async def main():
    await startcogs()
    await bot.start(defaultConfig.DISCORD_SDK)

asyncio.run(main())
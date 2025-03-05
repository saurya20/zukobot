import configs.DefaultConfig as defaultConfig
from discord.ext import commands
import google.generativeai as genai
import re

genai.configure(api_key=defaultConfig.GEMINI_SDK)
DISCORD_MAX_MESSAGE_LENGTH=2000
PLEASE_TRY_AGAIN_ERROR_MESSAGE='There was an issue with your question please try again.. '

class GeminiAgent(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.model = genai.GenerativeModel('gemini-pro')

    @commands.Cog.listener()
    async def on_message(self,msg):
        try:
            if msg.content == "ping gemini-agent":
                await msg.channel.send("Agent is connected..")
        except Exception as e:
            return PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e)

    @commands.command()
    async def query(self,ctx,question):
        try:
            response = self.gemini_generate_content(question)
            await ctx.send(response)
        except Exception as e:
            await ctx.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))

    @commands.command()
    async def pm(self,ctx):
        dmchannel = await ctx.author.create_dm()
        await dmchannel.send('Hi how can I help you today?')

    def gemini_generate_content(self,content):
        try:
            response = self.model.generate_content(content)
            return response
        except Exception as e:
            return PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e)


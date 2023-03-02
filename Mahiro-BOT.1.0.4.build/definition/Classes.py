import discord
from discord.ext import commands
#初始化
class Cog_Extension(commands.Cog):
    def __init__(self,bot: discord.Bot) :
        self.bot = bot

import os
import discord
from datetime import datetime
from discord.commands import slash_command
from discord.ext import commands
from definition.Classes import Cog_Extension
from pythonping import ping
import json

with open("config.json" , "r" ,encoding="utf8") as configFiles:  
    config = json.load(configFiles)

class Delay(Cog_Extension):
    # DELAY
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Delay已載入')
    @slash_command(name="延遲", description="查看機器人延遲時間")
    async def delay(self, ctx):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'{day}-正在連接主機')
        await ctx.response.defer()
        embed=discord.Embed(title="Mahiro-BOT",timestamp=datetime.now())
        embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
        if self.bot.latency * 1000 <= 1000:
            embed.color = 0x28FF28
        else:
            embed.color = 0xAE0000
        embed.add_field(name="BOT目前延遲", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        if self.bot.latency * 1000 <= 1000:
            embed.add_field(name="目前", value=":green_circle:-連線正常", inline=False)
        else:
            embed.add_field(name="目前", value=":red_circle:-連線超時", inline=False)
        await ctx.followup.send(embed=embed)

def setup(bot):
    bot.add_cog(Delay(bot))
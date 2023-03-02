import discord
from discord import message
from discord.commands import slash_command
from discord import option
from discord.ext import commands
from definition.Classes import Cog_Extension
from datetime import datetime
import socket
import asyncio
import json

class Update(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Update已載入')
    @slash_command(name="更新", description="查看今日更新日誌")
    @option("日期", description="日期", 
    choices=["2023-02-06","2023-02-08","2023-02-11","2023-02-20","2023-02-21","2023-02-23","2023-03-02"
    ])
    async def update(self, ctx, 日期:str):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'{day}-更新日誌')
        match 日期:
            case '2023-02-06':
                embed=discord.Embed(title="Mahiro-BOT",description="以下為2023-02-06更新日誌", color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = "更新", value="版本號為v1.0-b1", inline=False)
                embed.add_field(name = "", value="ParrotXray的機器人上線", inline=False)
                await ctx.respond(embed=embed, ephemeral = False)
            case '2023-02-08':
                embed=discord.Embed(title="Mahiro-BOT",description="以下為2023-02-08更新日誌", color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = "更新", value="版本號為v1.0-b2", inline=False)
                embed.add_field(name = "", value="新增星座運勢模組，用法:/星座運勢", inline=False)
                await ctx.respond(embed=embed, ephemeral = False)
            case '2023-02-11':
                embed=discord.Embed(title="Mahiro-BOT",description="以下為2023-02-11更新日誌", color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = "更新", value="版本號為v1.0-b3", inline=False)
                embed.add_field(name = "", value="修改星座運勢模組因超時連接所造成機器人程序終止問題", inline=False)
                await ctx.respond(embed=embed, ephemeral = False)
            case '2023-02-20':
                embed=discord.Embed(title="Mahiro-BOT",description="以下為2023-02-20更新日誌", color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = "更新", value="版本號為v1.0", inline=False)
                embed.add_field(name = "", value="機器人正式上線運作", inline=False)
                await ctx.respond(embed=embed, ephemeral = False)
            case '2023-02-21':
                embed=discord.Embed(title="Mahiro-BOT",description="以下為2023-02-21更新日誌", color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = "更新", value="版本號為v1.0.1", inline=False)
                embed.add_field(name = "", value="替換YT音樂播放庫", inline=False)
                await ctx.respond(embed=embed, ephemeral = False)
            case '2023-02-23':
                embed=discord.Embed(title="Mahiro-BOT",description="以下為2023-02-23更新日誌", color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = "更新", value="版本號為v1.0.3", inline=False)
                embed.add_field(name = "", value="2.修復音樂模組部分url無法播放問題", inline=False)
                embed.add_field(name = "", value="3.新增指令/音樂-網路電台", inline=False)
                embed.add_field(name = "", value="5.加入音樂風面圖標及時間戳", inline=False)
                embed.add_field(name = "", value="6.幫助指令分類，更易讀", inline=False)
                embed.add_field(name = "", value="7.大量指令優化及美化", inline=False)
            case '2023-03-02':
                embed=discord.Embed(title="Mahiro-BOT",description="以下為2023-03-02更新日誌", color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = "更新", value="版本號為v1.0.4", inline=False)
                embed.add_field(name = "", value="1.改變/圖片搜尋方法", inline=False)
                embed.add_field(name = "", value="2.加入**/客服單**指令", inline=False)
                embed.add_field(name = "", value="3.新增**/加入訊息 + 頻道、/退出訊息 + 頻道**訊息指令", inline=False)
                await ctx.respond(embed=embed, ephemeral = False)
def setup(bot):
    bot.add_cog(Update(bot))
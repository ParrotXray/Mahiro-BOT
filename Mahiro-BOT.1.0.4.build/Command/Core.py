import os
import discord
from discord.ext import commands
from discord.commands import slash_command
from discord import option
from definition.Classes import Cog_Extension
import asyncio
from datetime import datetime
from discord.ui import Select,View

class Core(Cog_Extension):
    # LOAD
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Core已載入')
    # RELOAD
    @slash_command(name="重載", description="重載模組")
    @option("模組", description="模組", 
    choices=["all", "Delay","Weather","Earthquake","Music","Info","Update","Password","Constellation","Userinfo","Serverinfo","Pixiv"])
    async def reload(self,ctx,模組:str):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-模組重載')
        await ctx.response.defer()
        if 模組 == "all":
            for Filename in os.listdir("./Command"):
                if Filename.endswith(".py"):
                    self.bot.reload_extension(f"Command.{Filename[:-3]}")
            embed=discord.Embed(title="Discord Bot Status", color=0xf4a5c3)
            embed.add_field(name="Reload", value="重新加載所有模組成功", inline=False)
            await ctx.followup.send(embed=embed)
            await asyncio.sleep(3)
            os.system('clear')
            print ('💠已重新載入')
        elif os.path.isfile(f"./Command/{模組}.py")!=True:
            embed=discord.Embed(title="Discord Bot Status", color=0xf4a5c3)
            embed.add_field(name="Reload", value="錯誤 該模組不存在", inline=False)
            await ctx.followup.send(embed=embed)
        else:
            self.bot.reload_extension(f"Command.{模組}")
            embed=discord.Embed(title="Discord Bot Status", color=0xf4a5c3)
            embed.add_field(name="Reload", value=f"重新加載{模組}模組成功", inline=False)
            await ctx.followup.send(embed=embed)
            await asyncio.sleep(3)
            os.system('clear')
            print ('💠已重新載入')
    # HELP
    @slash_command(name="幫助", description="查看指令列表")
    async def help(self,ctx):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Help使用')
        select = Select(
            placeholder="請選擇功能",
            options=[
                discord.SelectOption(
                    label="一般指令",
                    description = "沒有什麼功能的指令",
                    emoji= "📋"

                ),
                discord.SelectOption(
                    label="功能指令",
                    description = "有點實用功能的指令",
                    emoji= "📔"
                ),
                discord.SelectOption(
                    label="音樂指令",
                    description = "播放音樂功能的指令",
                    emoji= "🎵"
                ),
            ]
        )
        async def help_menu(interaction):
            match select.values[0]:
                case '一般指令':
                    embed=discord.Embed(title="__**一般指令列表**__", color=0xf4a5c3,timestamp=datetime.now())
                    embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                    embed.set_author(name="Mahiro-BOT", icon_url=self.bot.user.avatar.url)
                    embed.add_field(name="/幫助", value="顯示此則訊息", inline=True)
                    embed.add_field(name="/簡介", value="顯示機器人資訊", inline=True)
                    embed.add_field(name="/重載 + All/Name", value="重新加載所有/指定模組", inline=True)
                    embed.add_field(name="/延遲", value="取得機器人延遲時間", inline=True)
                    embed.add_field(name="/加入訊息 + 頻道、/退出訊息 + 頻道", value="新增加入、退出訊息傳送點", inline=True)
                case '功能指令':
                    embed=discord.Embed(title="__**功能指令列表**__", color=0xf4a5c3,timestamp=datetime.now())
                    embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                    embed.set_author(name="Mahiro-BOT", icon_url=self.bot.user.avatar.url)
                    embed.add_field(name="/天氣", value="取得各縣市天氣預報", inline=True)
                    embed.add_field(name="/地震", value="取得地震資訊", inline=True)
                    embed.add_field(name="/密碼", value="生成密碼", inline=True)
                    embed.add_field(name="/星座運勢", value="查看今日星座運勢", inline=True)
                    embed.add_field(name="/詢問", value="詢問問題", inline=True)
                    embed.add_field(name="/圖片", value="隨機圖片", inline=True)
                    embed.add_field(name="/客服單", value="建立客服單", inline=True)
                case '音樂指令':
                    embed=discord.Embed(title="__**音樂指令列表**__", color=0xf4a5c3,timestamp=datetime.now())
                    embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                    embed.set_author(name="Mahiro-BOT", icon_url=self.bot.user.avatar.url)
                    embed.add_field(name="/音樂-播放", value="播放歌曲", inline=True)
                    embed.add_field(name="/音樂-暫停播放", value="暫停當前正在播放的歌曲", inline=True)
                    embed.add_field(name="/音樂-繼續播放", value="繼續播放歌曲", inline=True)
                    embed.add_field(name="/音樂-跳過播放", value="跳過當前正在播放的歌曲", inline=True)
                    embed.add_field(name="/音樂-播放列表", value="顯示隊列中的當前歌曲", inline=True)
                    embed.add_field(name="/音樂-刪除指定歌曲", value="從隊列中刪除指定的歌曲", inline=True)
                    embed.add_field(name="/音樂-清除所有歌曲", value="清除整個隊列", inline=True)
                    embed.add_field(name="/音樂-顯示當前播放", value="顯示當前播放的歌曲", inline=True)
                    embed.add_field(name="/音樂-播放音量 + 聲音大小", value="顯示當前播放的音量及改變播放音量", inline=True)
                    embed.add_field(name="/音樂-離開語音", value="離開語音頻道", inline=False)

            await interaction.response.send_message(embed=embed)
            
        select.callback = help_menu
        view = View()
        view.add_item(select)
        await ctx.respond("📡以下為指令分類",view = view)

def setup(bot):
    bot.add_cog(Core(bot))
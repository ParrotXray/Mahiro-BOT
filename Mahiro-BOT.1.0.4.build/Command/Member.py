import discord
from discord import message
from discord.commands import slash_command
from discord import option
from discord.ext import commands
from definition.Classes import Cog_Extension
from datetime import datetime
import json
import os

class Member(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Member已載入')

    @slash_command(name="加入訊息", description="新增加入訊息傳送點")
    @option("頻道", description="請輸入一個有效的頻道")
    async def set_welcome(self, ctx,頻道:discord.TextChannel):
        welcome_file_path = os.path.join("database", "welcome.json")
        with open(welcome_file_path, "r") as file:
            data= json.load(file)
        data[str(ctx.guild.id)] = 頻道.id
        with open(welcome_file_path, "w") as file:
            json.dump(data,file,indent=4)
        embed=discord.Embed(title="Mahiro-BOT", color=0xf4a5c3, timestamp=datetime.now())
        embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
        embed.add_field(name = "資料更新成功", value=f"頻道為<#{頻道.id}>", inline=False)
        await ctx.respond(embed=embed)

    @slash_command(name="退出訊息", description="新增退出訊息傳送點")
    @option("頻道", description="請輸入一個有效的頻道")
    async def set_leave(self, ctx,頻道:discord.TextChannel):
        leave_file_path = os.path.join("database", "leave.json")
        with open(leave_file_path, "r") as file:
            data= json.load(file)
        data[str(ctx.guild.id)] = 頻道.id
        with open(leave_file_path, "w") as file:
            json.dump(data,file,indent=4)
        embed=discord.Embed(title="Mahiro-BOT", color=0xf4a5c3, timestamp=datetime.now())
        embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
        embed.add_field(name = "資料更新成功", value=f"頻道為<#{頻道.id}>", inline=False)
        await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(Member(bot))
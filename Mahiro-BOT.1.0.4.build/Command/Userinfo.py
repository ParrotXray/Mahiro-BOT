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

class Userinfo(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Userinfo已載入')
    @slash_command(name="用戶信息", description="查看用戶信息")
    @option('使用者', discord.Member, description='查看用戶信息')
    async def userinfo(self, ctx,使用者=None):
            author = 使用者 or ctx.author
            
            embed = discord.Embed(title=f"{author}的資訊",
                        colour=author.colour,
                        timestamp=datetime.now())
            embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
            if author.bot == True:
                bot_author = "是"
            elif author.bot == False:
                bot_author = "否"
            else:
                bot_author = ""
            
            if bool(author.premium_since) == True:
                premium_since = "是"
            elif bool(author.premium_since) == False:
                premium_since = "否"
            else:
                premium_since = ""
            
            match str(author.status).title():
                case 'Offline':
                    author_status = '⚪'
                case 'Idle':
                    author_status = '🟠'
                case 'Dnd':
                    author_status = '🔴'
                case 'Online':
                    author_status = '🟢'
                case None:
                    author_status = ''
            if author.activity:
                match str(author.activity.type).split('.')[-1].title():
                    case 'Playing':
                        activity_type = "正在玩"
                    case 'Streaming':
                        activity_type = "正在直播"
                    case 'Listening':
                        activity_type = "正在聽"
                    case 'Watching':
                        activity_type = "正在看"
                    case 'Competing':
                        activity_type = "正在競爭"
                    case 'Custom':
                        activity_type = ""
            else:
                activity_type = ""

            try:
                embed.set_thumbnail(url=author.avatar.url)
                fields = [("👤名字", str(author), True),
                        ("🪪ID", f'`{author.id}`', True),
                        ("⚙️是否為機器人", bot_author, True),
                        ("👥身分組", author.top_role.mention, True),
                        ("💥狀態", author_status, True),
                        ("🚨活動", f"{activity_type if author.activity else '無'} {author.activity.name if author.activity else ''}", True),
                        ("⏰創建時間", author.created_at.strftime("%Y/%m/%d %H:%M:%S"), True),
                        ("⏱️加入時間", author.joined_at.strftime("%Y/%m/%d %H:%M:%S"), True),
                        ("🚀伺服器加成用戶", premium_since, True)]
            
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
            except:
                embed.set_thumbnail(url='https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x225.jpg')
                fields = [("👤名字", str(author), True),
                        ("🪪ID", f'`{author.id}`', True),
                        ("⚙️是否為機器人", bot_author, True),
                        ("👥身分組", author.top_role.mention, True),
                        ("💥狀態", author_status, True),
                        ("🚨活動", f"{activity_type if author.activity else '無'} {author.activity.name if author.activity else ''}", True),
                        ("⏰創建時間", author.created_at.strftime("%Y/%m/%d %H:%M:%S"), True),
                        ("⏱️加入時間", author.joined_at.strftime("%Y/%m/%d %H:%M:%S"), True),
                        ("🚀伺服器加成用戶", premium_since, True)]
            
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
            await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(Userinfo(bot))
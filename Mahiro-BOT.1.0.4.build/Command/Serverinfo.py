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
class Serverinfo(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Serverinfo已載入')
    @slash_command(name="伺服器信息", description="查看伺服器信息")
    async def serverinfo(self, ctx: commands.Context):
        guild = ctx.guild
        statuses = [len(list(filter(lambda m: str(m.status) == "online", guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", guild.members)))]

        embed = discord.Embed(title=f"{guild.name} ({guild.id})", description=f"{str(guild.member_count)} 位成員", color=0xf4a5c3, timestamp=datetime.now())
        embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
        try:
            embed.set_thumbnail(url=guild.icon.url)
            fields = [("🪪ID", f'`{guild.id}`', True),
                    ("👑擁有者", guild.owner, True),
                    ("⏰建立時間", guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                    ("👤成員數", len(guild.members), True),
                    ("👥一般成員數", len(list(filter(lambda m: not m.bot, guild.members))), True),
                    ("⚙️機器人成員數", len(list(filter(lambda m: m.bot, guild.members))), True),
                    ("💥成員狀態", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                    ("💬文字頻道數", len(guild.text_channels), True),
                    ("📣語音頻道數", len(guild.voice_channels), True),
                    ("💎頻道分類數", len(guild.categories), True),
                    ("💠身分組數", len(guild.roles), True),
                    ("🏵️邀請數", len(await guild.invites()), True),
                    ("\u200b", "\u200b", True)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        except:
            embed.set_thumbnail(url='https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x225.jpg')
            fields = [("🪪ID", f'`{guild.id}`', True),
                    ("👑擁有者", guild.owner, True),
                    ("⏰建立時間", guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                    ("👤成員數", len(guild.members), True),
                    ("👥一般成員數", len(list(filter(lambda m: not m.bot, guild.members))), True),
                    ("⚙️機器人成員數", len(list(filter(lambda m: m.bot, guild.members))), True),
                    ("💥成員狀態", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                    ("💬文字頻道數", len(guild.text_channels), True),
                    ("📣語音頻道數", len(guild.voice_channels), True),
                    ("💎頻道分類數", len(guild.categories), True),
                    ("💠身分組數", len(guild.roles), True),
                    ("🏵️邀請數", len(await guild.invites()), True),
                    ("\u200b", "\u200b", True)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(Serverinfo(bot))
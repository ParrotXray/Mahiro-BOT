import discord
from discord import message
from discord.commands import slash_command
from discord.ext import commands
from definition.Classes import Cog_Extension
from datetime import datetime
from discord.ui import Button,View

class Info(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Info已載入')
    @slash_command(name="簡介", description="Bot簡介")
    async def info(self, ctx):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'{day}-內容')
        button_dc = Button(label="👥邀請",style=discord.ButtonStyle.url,url="https://discord.com/api/oauth2/authorize?client_id=1064535925956300850&permissions=8&scope=bot%20applications.commands")
        button_pixiv = Button(label="💥欣賞我的作品",style=discord.ButtonStyle.url,url="https://www.pixiv.net/users/59922240")
        view = View()
        view.add_item(button_dc)
        view.add_item(button_pixiv)
        embed=discord.Embed(title="Mahiro-BOT",color=0xf4a5c3,timestamp=datetime.now())
        embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
        embed.add_field(name = "內容", value="此為ParrotXray自學自行開發的BOT，歡迎加我", inline=False)
        await ctx.response.send_message(embed=embed, view=view)
def setup(bot):
    bot.add_cog(Info(bot))
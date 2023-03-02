import discord
import asyncio
import requests
from discord.ext import commands
import os
import json
from pythonping import ping
from datetime import datetime
import socket
#py-cord2.3.2
with open("config.json" , "r" ,encoding="utf8") as configFiles:  
    config = json.load(configFiles)

socket.setdefaulttimeout(10)

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

print("Mahiro機器人啟動中...")

@bot.event
async def on_member_join(member):
    welcome_file_path = os.path.join("database", "welcome.json")
    with open(welcome_file_path, "r") as file:
        data= json.load(file)
    if str(member.guild.id) in data:
        channel = bot.get_channel(data[str(member.guild.id)])
        embed=discord.Embed(title=member.guild, color=0xf4a5c3, timestamp=datetime.now())
        try:
            embed.set_thumbnail(url=member.avatar.url)
        except:
            embed.set_thumbnail(url='https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x225.jpg')
        embed.set_footer(text="Mahiro-BOT",icon_url=bot.user.avatar.url)
        embed.add_field(name = "", value=f"🎉{member} 歡迎加入", inline=False)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    leave_file_path = os.path.join("database", "leave.json")
    with open(leave_file_path, "r") as file:
        data= json.load(file)
    if str(member.guild.id) in data:
        channel = bot.get_channel(data[str(member.guild.id)])
        embed=discord.Embed(title=member.guild, color=0xf4a5c3, timestamp=datetime.now())
        try:
            embed.set_thumbnail(url=member.avatar.url)
        except:
            embed.set_thumbnail(url='https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x225.jpg')
        embed.set_footer(text="Mahiro-BOT",icon_url=bot.user.avatar.url)
        embed.add_field(name = "", value=f"👋{member} 離開了", inline=False)
        await channel.send(embed=embed)

@bot.event
async def on_ready():
    os.system('clear')
    print("-"*15)
    print("🌐Mahiro機器人上線")
    print("💠BOT版本v1.0.4")
    print("-"*15)
    print(bot.user.name)
    print(bot.user.id)
    print(bot.user)
    print("-"*15)
    Activity = discord.Activity(type=discord.ActivityType.watching,name="使用 /幫助")
    await bot.change_presence(activity=Activity)


def load():
    # still doesn't need to be async
    for filename in os.listdir('./Command'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'Command.{filename[:-3]}')
                print(f'✅   已加載 {filename}')
            except Exception as error:
                print(f'❎   {filename} 錯誤 {error}')


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

load()
bot.run(config["Token"])
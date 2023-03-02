import requests
import discord
import asyncio
from discord import message
from discord.ext import commands
from discord.commands import slash_command
from discord import option
from definition.Classes import Cog_Extension
from datetime import datetime
import json
now = datetime.now()
day=now.strftime("%Y-%m-%d %H:%M:%S")

with open("config.json" , "r" ,encoding="utf8") as configFiles:  
    config = json.load(configFiles)

APIToken = config["APIToken"]

class Earthquake(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Earthquake已載入')

    @slash_command(name="地震", description="地震報告")
    @option("類型", description="類型", 
    choices=["大型地震", "小型地震"
    ])
    async def earthquake(self,ctx, 類型:str):
        await ctx.response.defer()
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={APIToken}'
        small_url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={APIToken}'
        response = requests.get(url)
        small_response = requests.get(small_url)
        print(f'{day}-查詢Earthquake,狀態{response.status_code},{small_response.status_code}')
        if response.status_code == 200 and small_response.status_code == 200:
            if 類型 == "大型地震":
                data_json = response.json()
                eq = data_json['records']['Earthquake']    # 轉換成 json 格式
                for i in eq:
                    loc = i['EarthquakeInfo']['Epicenter']['Location']        # 地震地點
                    val = i['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']  # 芮氏規模
                    dep = i['EarthquakeInfo']['FocalDepth']             # 地震深度
                    eq_time = i['EarthquakeInfo']['OriginTime']               # 地震時間
                    img = i['ReportImageURI']
                    msg = f'{loc}，芮氏規模 {val} 級，深度 {dep} 公里，發生時間 {eq_time}'
                    print(f'{day}-{msg}')
                    break
                embed=discord.Embed(title="Mahiro-BOT",description=f'{loc}',color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = ":star2:芮氏規模", value=f'{val}', inline=False)
                embed.add_field(name = ":boom:深度", value=f'{dep}公里', inline=False)
                embed.add_field(name = ":stopwatch:發生時間", value=f'{eq_time}', inline=False)
                embed.set_image(url=img)
                await ctx.followup.send(embed=embed, ephemeral = False)
            elif 類型 == "小型地震":
                small_data_json = small_response.json()
                small_eq = small_data_json['records']['Earthquake']
                for i in small_eq:
                    small_loc = i['EarthquakeInfo']['Epicenter']['Location']       # 地震地點
                    small_val = i['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']  # 芮氏規模
                    small_dep = i['EarthquakeInfo']['FocalDepth']             # 地震深度
                    small_eq_time = i['EarthquakeInfo']['OriginTime']             # 地震時間
                    small_img = i['ReportImageURI']
                    small_msg = f'{small_loc}，芮氏規模 {small_val} 級，深度 {small_dep} 公里，發生時間 {small_eq_time}'
                    print(f'{day}-{small_msg}')
                    break
                embed=discord.Embed(title="Mahiro-BOT",description=f'{small_loc}',color=0xf4a5c3,timestamp=datetime.now())
                embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
                embed.add_field(name = ":star2:芮氏規模", value=f'{small_val}', inline=False)
                embed.add_field(name = ":boom:深度", value=f'{small_dep}公里', inline=False)
                embed.add_field(name = ":stopwatch:發生時間", value=f'{small_eq_time}', inline=False)
                embed.set_image(url=small_img)
                await ctx.followup.send(embed=embed, ephemeral = False)
        else:
            embed=discord.Embed(title="Mahiro-BOT", color=0xf4a5c3,timestamp=datetime.now())
            embed.set_footer(text=f"找不到資料,狀態{response.status_code},{small_response.status_code}",icon_url=self.bot.user.avatar.url)
            await ctx.followup.send(embed=embed)
def setup(bot):
    bot.add_cog(Earthquake(bot))
import requests
import re
from opencc import OpenCC
import discord
from discord import message
from discord.commands import slash_command
from discord import option
from discord.ext import commands
from definition.Classes import Cog_Extension
from datetime import datetime
from fake_useragent import UserAgent
import random
import asyncio

class Constellation(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Constellation已載入')
    @slash_command(name="星座運勢", description="查看今日星座運勢")
    @option("星座", description="星座", 
    choices=["水瓶座", "雙魚座",
    "白羊座","金牛座","雙子座","巨蟹座",
    "獅子座","處女座","天秤座",
    "天蠍座","射手座","摩羯座"
    ])
    async def constellation(self, ctx, 星座:str):
        response_Constellation = None
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        cc = OpenCC('s2twp')
        delay_choices = [3, 5, 8, 10]  #延遲的秒數
        delay = random.choice(delay_choices) 
        await ctx.response.defer()

        match 星座:
            case '水瓶座':
                constellation ="aquarius"
                星座 = ":aquarius: 水瓶座"
            case '雙魚座':
                constellation = "pisces"
                星座 = ":pisces: 雙魚座"
            case '白羊座':
                constellation = "aries"
                星座 = ":aries: 白羊座"
            case '金牛座':
                constellation = "taurus"
                星座 = ":taurus: 金牛座"
            case '雙子座':
                constellation = "gemini"
                星座 = ":gemini: 雙子座"
            case '巨蟹座':
                constellation = "cancer"
                星座 = ":cancer: 巨蟹座"
            case '獅子座':
                constellation = "leo"
                星座 = ":leo: 獅子座"
            case '處女座':
                constellation = "virgo"
                星座 = ":virgo: 處女座"
            case '天秤座':
                constellation = "libra"
                星座 = ":libra: 天秤座"
            case '天蠍座':
                constellation = "scorpio"
                星座 = ":scorpius: 天蠍座"
            case '射手座':
                constellation = "sagittarius"
                星座 = ":sagittarius: 射手座"
            case '摩羯座':
                constellation = "capricorn"
                星座 = ":capricorn: 摩羯座"
        
        user_agent = UserAgent()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
            "Accept-Encoding": "gzip, deflate, br", 
            "Accept-Language": "zh-TW,zh;q=0.9", 
            "Host": "www.xzw.com",  #目標網站
            "Sec-Fetch-Dest": "document", 
            "Sec-Fetch-Mode": "navigate", 
            "Sec-Fetch-Site": "none", 
            "Upgrade-Insecure-Requests": "1", 
            "User-Agent": user_agent.random, #使用者代理
            "Referer": f'https://www.xzw.com/fortune/{constellation}/'
        }
        try:
            response_Constellation = requests.get(url = f'https://www.xzw.com/fortune/{constellation}/', headers=headers, timeout=10)
            await asyncio.sleep(delay)
            response_Constellation.encoding = "utf-8"
            content = response_Constellation.text
            print(f'{day}-查詢星座運勢,狀態{response_Constellation.status_code}')
            request = True
        except requests.exceptions.RequestException as error:
            print(f'{day}-{error}')
            embed=discord.Embed(title="Mahiro-BOT", color=0xf4a5c3)
            embed.set_footer(text="連接超時，請等會在試")
            await ctx.followup.send(embed=embed,delete_after = 5)
            request = False

        if response_Constellation.status_code == 200 and request == True:
            lis = re.findall('<em style=" width:(.*?)px;">',content)

            comprehensive_fortune,love_fortune,career_fortune,wealth_fortune = [str(int(int(i)/16))+"星" for i in lis]

            health_index = re.findall('健康指数：</label>(.*?)<',content,re.S)[0]

            negotiation_Index = re.findall('商谈指数：</label>(.*?)<',content,re.S)[0]

            lucky_color = re.findall('幸运颜色：</label>(.*?)<',content,re.S)[0]

            lucky_num = re.findall('幸运数字：</label>(.*?)<',content,re.S)[0]

            match_constellation = re.findall('速配星座：</label>(.*?)<',content,re.S)[0]

            short_comment = re.findall('短评：</label>(.*?)<',content,re.S)[0]

            detail_comprehensive_fortune = re.findall('综合运势</strong><span>(.*?)<small>',content,re.S)[0]

            detail_love_fortune = re.findall('爱情运势</strong><span>(.*?)</span>',content,re.S)[0]

            detail_career = re.findall('事业学业</strong><span>(.*?)</span>',content,re.S)[0]

            detail_wealth = re.findall('财富运势</strong><span>(.*?)</span>',content,re.S)[0]

            detail_wealth_fortune = re.findall('健康运势</strong><span>(.*?)</span>',content,re.S)[0]

            embed=discord.Embed(title="Mahiro-BOT",description=f'**{星座}**-今日運勢總覽', color=0xf4a5c3, timestamp=datetime.now())
            embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)

            embed.add_field(name = ":star2: 綜合運勢:", value=comprehensive_fortune, inline=False)
            embed.add_field(name = ":heart: 愛情運勢:", value=love_fortune, inline=True)
            embed.add_field(name = ":dollar: 事業運勢:", value=career_fortune, inline=True)
            embed.add_field(name = ":bust_in_silhouette: 健康運勢:",value=wealth_fortune, inline=True)

            embed.add_field(name = ":pill: 健康指數:", value=health_index, inline=True)
            embed.add_field(name = ":six_pointed_star: 商談指數:", value=negotiation_Index, inline=True)
            embed.add_field(name = ":1234: 幸運數字:", value=lucky_num, inline=True)
            embed.add_field(name = ":heart_decoration: 幸運顏色:",value=cc.convert(lucky_color), inline=True)
            embed.add_field(name = ":restroom: 速配星座:", value=cc.convert(match_constellation), inline=True)
            embed.add_field(name = ":sparkle: 短評:", value=cc.convert(short_comment), inline=True)

            embed.add_field(name = ":sparkles: 你的【綜合運勢】詳細說明:", value=cc.convert(detail_comprehensive_fortune), inline=False)
            embed.add_field(name = ":sparkles: 你的【愛情運勢】詳細說明:", value=cc.convert(detail_love_fortune), inline=False)
            embed.add_field(name = ":sparkles: 你的【事業學業】詳細說明:", value=cc.convert(detail_career), inline=False)
            embed.add_field(name = ":sparkles: 你的【財富運勢】詳細說明:",value=cc.convert(detail_wealth), inline=False)
            embed.add_field(name = ":sparkles: 你的【健康運勢】詳細說明:", value=cc.convert(detail_wealth_fortune), inline=False)

            await ctx.followup.send(embed=embed, ephemeral = False)

        else:
            embed=discord.Embed(title="Mahiro-BOT", color=0xf4a5c3)
            embed.set_footer(text=f"找不到資料,狀態{response_Constellation.status_code}")
            await ctx.followup.send(embed=embed)



def setup(bot):
    bot.add_cog(Constellation(bot))
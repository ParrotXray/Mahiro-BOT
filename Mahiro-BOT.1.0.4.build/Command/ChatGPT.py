import discord
from discord import message
from discord.commands import slash_command
from discord import option
from discord.ext import commands
from definition.Classes import Cog_Extension
from datetime import datetime
import requests
import re
from opencc import OpenCC
import openai
from fake_useragent import UserAgent

user_agent = UserAgent()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "zh-TW,zh;q=0.9", 
    "Host": "api.aa1.cn",  #目標網站
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "none", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": user_agent.random, #使用者代理
    "Referer": "https://www.google.com/"
}

class ChatGPT(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-ChatGPT已載入')
    @slash_command(name="詢問", description="詢問問題")
    @option("問題", description="請輸入問題")
    async def chat(self, ctx, 問題):
        await ctx.response.defer()
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'{day}-詢問問題')
        cc = OpenCC('s2twp')
        response_chat = requests.get(url = f'https://v1.apigpt.cn/?q={問題}&apitype=sql')
        if response_chat.status_code == 200 :
            data_json_chat = response_chat.json()
            #print(data_json_chat['msg'])
            if data_json_chat['msg'] =='获取成功' or data_json_chat['msg'] is None :
                html = cc.convert(data_json_chat['ChatGPT_Answer'])
                embed=discord.Embed(title="Mahiro-BOT",description=f"詢問-**{問題}**", color=0xf4a5c3, timestamp=datetime.now())
                embed.set_footer(text='請各位不要問政治敏感、色情低俗、賭、毒等違法內容，可能存在誤攔',icon_url=self.bot.user.avatar.url)
                embed.add_field(name = "結果", value='```' + html + '```', inline=False)
                await ctx.followup.send(embed=embed, ephemeral = False)
            
            elif data_json_chat['msg'] == '获取失败，请重试' or data_json_chat['msg'] !='获取成功' or data_json_chat['msg'] != '获取失败，请重试':
                response = requests.get(url = 'https://api.aa1.cn/special/chatgpt', headers=headers, timeout=10)
                response.encoding = "utf-8"
                if response.status_code == 200:
                    html_content = response.text
                    result = re.findall(r'免费密钥：(\S+)', html_content)
                    #print(result[0])
                    try:
                        openai.api_key = result[0]
                        response = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt=問題,
                            max_tokens=2048,
                            temperature=1,
                        )
                        response_lines = response["choices"][0]["text"]
                        if response_lines is None:
                            await ctx.followup.send('問題有誤，請檢查格式及問題')
                        else:
                            embed=discord.Embed(title="Mahiro-BOT",description=f"詢問-**{問題}**", color=0xf4a5c3)
                            embed.set_footer(text='請各位不要問政治敏感、色情低俗、賭、毒等違法內容，可能存在誤攔。',icon_url=self.bot.user.avatar.url)
                            embed.add_field(name = "結果", value='```' + response_lines + '```', inline=False)
                            await ctx.followup.send(embed=embed, ephemeral = False)
                    except Exception as e:
                        print(e)
                        await ctx.followup.send("API無響應，請重試")

        else:
            await ctx.followup.send("請求失敗")

def setup(bot):
    bot.add_cog(ChatGPT(bot))
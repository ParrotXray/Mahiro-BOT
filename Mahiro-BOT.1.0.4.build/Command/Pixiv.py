from pixivpy3 import *
import random
import discord
from discord import message
from discord.ext import commands
from discord.commands import slash_command
from discord import option
from definition.Classes import Cog_Extension
from datetime import datetime
from discord.ui import Button,View
import re
import asyncio
import json

with open("config.json" , "r" ,encoding="utf8") as configFiles:  
    config = json.load(configFiles)

api = AppPixivAPI()
api.auth(refresh_token=config["Pixiv_Token"])

class Pixiv(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Pixiv已載入')
        await asyncio.sleep(3)
        while True:
            try:
                global output_update_token
                output_update_token = []
                output_update_token.clear()
                next_qs_update_token = {"user_id": 59922240}
                while next_qs_update_token :
                    json_update_token = api.user_illusts(**next_qs_update_token)
                    for illust in json_update_token.illusts:
                        now = datetime.now()
                        day=now.strftime("%Y-%m-%d %H:%M:%S")
                        user_update_token = illust.user['name'] 
                        title_update_token = illust.title
                        id_update_token = illust.id
                        image_urls_update_token = illust.image_urls['large']
                        profile_image_urls_update_token = illust.user['profile_image_urls']['medium']
                        output_update_token.append((user_update_token ,title_update_token ,image_urls_update_token, profile_image_urls_update_token,id_update_token))
                    next_qs_update_token = api.parse_qs(json_update_token.next_url)
                    print (f'{day}-更新最新作品{output_update_token[0]}')
            except:
                print (f'{day}-Token過期')
            await asyncio.sleep(300)

    @slash_command(name="圖片", description="隨機圖片")
    @option("關鍵字", description="請輸入關鍵字")
    async def pixiv(self, ctx, 關鍵字 = None):
        if 關鍵字 is None:
            choices = ['お兄ちゃんはおしまい', '緒山真尋', 'おにまい', '緒山まひろ', '穂月もみじ', '穂月かえで', '桜花あさひ', '室崎みよ', '緒山みはり']
            關鍵字 = random.choice(choices)
        output_list = []
        random_number = 0
        i=0
        random_number = random.randint(0, 200)
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'{day}-隨選數{random_number},隨選關鍵字{關鍵字}')
        await ctx.defer()
        #next_qs = {"word": 關鍵字,"search_target":"exact_match_for_tags"}
        next_qs = {"word": 關鍵字}
        try:
            while next_qs :
                json_result = api.search_illust(**next_qs)
                if i <= random_number:
                    for illust in json_result.illusts:
                        if i <= random_number:
                            user = illust.user['name'] 
                            title = illust.title
                            id = illust.id
                            image_urls = illust.image_urls['large']
                            profile_image_urls = illust.user['profile_image_urls']['medium']
                            output_list.append((user ,title ,image_urls, profile_image_urls,id))
                            #print((user ,title ,image_urls, profile_image_urls,id),i)
                            i += 1
                            next_qs = api.parse_qs(json_result.next_url)
                        else:
                            break
                else:
                    break
        except:
            await ctx.followup.send("讓我休息一下")
        if output_list:
            random_output = random.choice(output_list)
            user = random_output[0]
            title = random_output[1]
            image_urls = random_output[2]
            profile_image_urls = random_output[3]
            id = random_output[4]
            #api.download(image_urls)
            Pixiv_image_urls = re.search(r'https://i\.pximg\.net/(.*)', image_urls)
            if Pixiv_image_urls:
                image_urls = Pixiv_image_urls.group(1)
            Pixiv_profile_image_urls = re.search(r'https://i\.pximg\.net/(.*)', profile_image_urls)
            if Pixiv_profile_image_urls:
                profile_image_urls = Pixiv_profile_image_urls.group(1)

            button = Button(label="🖼️查看圖片",style=discord.ButtonStyle.url,url=f"https://www.pixiv.net/artworks/{id}")
            view = View()
            view.add_item(button)

            embed=discord.Embed(title="Mahiro-BOT", description=f"作者-**{user}**", color=0xf4a5c3, timestamp=datetime.now())
            embed.set_footer(text=f"來源:https://www.pixiv.net/artworks/{id}",icon_url='https://i.pixiv.cat/' + profile_image_urls)
            embed.add_field(name = "標題", value=f'{title}', inline=False)
            embed.set_image(url='https://i.pixiv.cat/' + image_urls)
            await ctx.followup.send(embed=embed, view=view)
            output_list.clear()
    @slash_command(name="我的作品", description="隨機我的作品")
    async def my_pixiv(self, ctx):
        await ctx.defer()
        if output_update_token:
            random_output_update_token = random.choice(output_update_token)
            user_update_token = random_output_update_token[0]
            title_update_token = random_output_update_token[1]
            image_urls_update_token = random_output_update_token[2]
            profile_image_urls_update_token = random_output_update_token[3]
            id_update_token = random_output_update_token[4]
            Pixiv_my_image_urls = re.search(r'https://i\.pximg\.net/(.*)', image_urls_update_token)
            if Pixiv_my_image_urls:
                image_urls_update_token = Pixiv_my_image_urls.group(1)
            Pixiv_profile_image_urls = re.search(r'https://i\.pximg\.net/(.*)', profile_image_urls_update_token)
            if Pixiv_profile_image_urls:
                profile_image_urls_update_token = Pixiv_profile_image_urls.group(1)
            
            button_update_token = Button(label="🖼️查看圖片",style=discord.ButtonStyle.url,url=f"https://www.pixiv.net/artworks/{id_update_token}")
            view = View()
            view.add_item(button_update_token)

            embed=discord.Embed(title="Mahiro-BOT", description=f"作者-**{user_update_token}**", color=0xf4a5c3, timestamp=datetime.now())
            embed.set_footer(text=f"來源:https://www.pixiv.net/artworks/{id_update_token}",icon_url='https://i.pixiv.cat/' + profile_image_urls_update_token)
            embed.add_field(name = "標題", value=f'{title_update_token}', inline=False)
            embed.set_image(url='https://i.pixiv.cat/' + image_urls_update_token)
            await ctx.followup.send(embed=embed, view=view)
def setup(bot):
    bot.add_cog(Pixiv(bot))


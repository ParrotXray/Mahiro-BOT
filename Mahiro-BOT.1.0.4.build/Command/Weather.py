import requests ,time
import discord
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
weather_url = f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization={APIToken}&downloadType=WEB&format=JSON'
significance_url = f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/W-C0033-001?Authorization={APIToken}&downloadType=WEB&format=JSON'
img_url = f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0058-003?Authorization={APIToken}&downloadType=WEB&format=JSON'
climate_url = f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization={APIToken}&downloadType=WEB&format=JSON'
aqi_url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
class Weather(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Weather已載入')
    @slash_command(name="天氣", description="查詢各地天氣")
    @option("城市", description="城市", 
    choices=["基隆市", "臺北市", "新北市",
    "桃園市","新竹市","新竹縣","苗栗縣",
    "臺中市","彰化縣","南投縣",
    "雲林縣","嘉義市","嘉義縣",
    "臺南市","高雄市","屏東縣",
    "臺東縣","花蓮縣","宜蘭縣",
    "澎湖縣","金門縣","連江縣"
    ])
    async def weather(self, ctx,城市:str):
        await ctx.response.defer()
        response_weather = requests.get(weather_url)
        response_significance = requests.get(significance_url)
        response_img = requests.get(img_url)
        response_climate = requests.get(climate_url)
        response_aqi = requests.get(aqi_url)
        print(f'{day}-查詢{城市}天氣,狀態{response_weather.status_code},{response_significance.status_code},{response_img.status_code},{response_climate.status_code},{response_aqi.status_code}')
        if response_weather.status_code == 200 and response_significance.status_code == 200 and response_img.status_code == 200 and response_climate.status_code == 200 and response_aqi.status_code == 200:
            data_json_weather = response_weather.json() # 轉換成 JSON 格式
            data_json_significance = response_significance.json()
            data_json_img = response_img.json()
            data_json_climate = response_climate.json()
            data_json_aqi = response_aqi.json()

            location_weather = data_json_weather['cwbopendata']['dataset']['location']
            location_significance = data_json_significance['cwbopendata']['dataset']['location'] 
            img = data_json_img['cwbopendata']['dataset']['resource']['uri']
            location_climate = data_json_climate['cwbopendata']['location']
            location_aqi = data_json_aqi['records']

            city_name = 城市
            for i in location_weather:
                if i['locationName'] == city_name:
                    city = i['locationName']    # 縣市名稱
                    wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
                    maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最高溫
                    mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最低溫
                    ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']    # 舒適度
                    pop8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']   # 降雨機率
                    break
            for i in location_significance:
                if i['locationName'] == city_name:
                    if i['hazardConditions'] is None:
                        phenomena = "無"
                        break
                    else:
                        phenomena = i['hazardConditions']['hazards']['info']['phenomena']
                    break
            temp_sum = 0
            humd_sum = 0
            r24_sum = 0
            num_stations = 0

            for i in location_climate:
                if i['parameter'][0]['parameterValue'] == city_name:
                    if i['weatherElement'][3]['elementValue']['value'] != "-99":
                        temp_sum += float(i['weatherElement'][3]['elementValue']['value'])
                    if i['weatherElement'][4]['elementValue']['value'] != "-99":
                        humd_sum += float(i['weatherElement'][4]['elementValue']['value'])
                    if i['weatherElement'][6]['elementValue']['value'] != "-99":
                        r24_sum += float(i['weatherElement'][6]['elementValue']['value'])
                    num_stations += 1
                    break
            city_temp = round(temp_sum / num_stations , 1)
            city_humd = round(humd_sum / num_stations , 1)
            city_r24 = r24_sum

            city_aqi_sum = 0
            city_aqi_count = 0
            for i in location_aqi:
                if i['county'] == city:
                    city_aqi_sum += int(i['aqi'])
                    city_aqi_count += 1
            city_aqi_average = round(city_aqi_sum / city_aqi_count, 1)
            if city_aqi_average >= 0 and city_aqi_average <= 50:
                status = "良好"
            elif city_aqi_average > 50 and city_aqi_average <= 100:
                status = "普通"
            elif city_aqi_average > 100 and city_aqi_average <= 150:
                status = "對敏感族群不健康"
            elif city_aqi_average > 150 and city_aqi_average <= 200:
                status = "對所有族群不健康"
            elif city_aqi_average > 200 and city_aqi_average <= 300:
                status = "非常不健康"
            elif city_aqi_average > 300 and city_aqi_average <= 500:
                status = "危害"
            else:
                status = "未知"

            embed=discord.Embed(title="Mahiro-BOT", color=0xf4a5c3,timestamp=datetime.now())
            #embed.set_thumbnail(url=img)
            embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
            embed.add_field(name = f':office:{city}', value=f'未來8小時{wx8}。降雨機率{pop8} %。最高溫{maxt8} °C。最低溫{mint8} °C。{ci8}。', inline=False)
            embed.add_field(name = ":fire:目前氣溫", value=f'{city_temp} °C', inline=True)
            embed.add_field(name = ":droplet:目前濕度", value=f'{city_humd} %', inline=True)
            embed.add_field(name = ":thunder_cloud_rain:累積雨量", value=f'{city_r24} mm', inline=True)
            embed.add_field(name = ":boom:AQI", value=f'{city_aqi_average}', inline=True)
            embed.add_field(name = ":dash:空氣品質", value=f'{status}', inline=True)
            embed.add_field(name = ":star2:警特報", value=f'{phenomena}', inline=True)
            embed.set_image(url=f'{img}?{time.time_ns()}')
            await ctx.followup.send(embed=embed)
        else:
            embed=discord.Embed(title="Mahiro-BOT", color=0xf4a5c3)
            embed.set_footer(text=f"找不到資料,狀態{response_weather.status_code},{response_significance.status_code},{response_img.status_code},{response_climate.status_code},{response_aqi.status_code}",icon_url=self.bot.user.avatar.url)
            await ctx.followup.send(embed=embed)

def setup(bot):
    bot.add_cog(Weather(bot))
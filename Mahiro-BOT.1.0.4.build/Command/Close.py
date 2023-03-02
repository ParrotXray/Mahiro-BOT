import asyncio
import json
import os
from typing import Any
from definition.Classes import Cog_Extension
import aiofiles
import discord
from discord.ext import commands
from datetime import datetime

class Close(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Close已載入')
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: Any) -> None:
        path = "database/close.json"
        if not os.path.isfile(path):  # 檢測是否有設置檔
            async with aiofiles.open(path, "w") as file:  # 創建新的設置檔
                await file.write(json.dumps({}, indent=4))
        if payload.member.bot or payload.emoji.name != "🔒":
            return
        async with aiofiles.open(path, "r") as file:  # 開啟關閉訊息資料檔案
            data = json.loads(await file.read())  # 載入資料
        if data[str(payload.channel_id)] != payload.message_id:  # 檢測該訊息是否是關閉訊息
            return  # 如果不是就結束運行
        channel = await self.bot.fetch_channel(payload.channel_id)  # 抓取該頻道資料
        await channel.send("客服單將在10秒後刪除")
        await asyncio.sleep(10)  # 等待10秒鐘
        await channel.delete(reason=f"由 {payload.member} 關閉客服單")
        async with aiofiles.open(path, "w") as file:
            del data[str(payload.channel_id)]  # 移除關閉訊息資料中的該頻道資料
            await file.write(json.dumps(data, indent=4))

def setup(bot):
    bot.add_cog(Close(bot))

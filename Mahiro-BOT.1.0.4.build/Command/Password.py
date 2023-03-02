import discord
from discord import message
from discord.commands import slash_command
from discord import option
from discord.ext import commands
from definition.Classes import Cog_Extension
from datetime import datetime
import random
import asyncio

class Password(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Password已載入')
    @slash_command(name="密碼", description="生成密碼")
    @option("多少數字",description="密碼要有多少數字")
    @option("多少符號",description="密碼要有多少符號")
    @option("多少字母",description="密碼要有多少字母")
    async def password(self, ctx, 多少數字:int,多少符號:int,多少字母:int):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'{day}-密碼以產生')
        if 多少數字+多少符號+多少字母 >= 1000:
            await ctx.respond('太長了')
        else:    
            user_id = ctx.author.id
            numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            symbols = ["~", "!", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "=", "/", "{", "}", "@", ",", "?", ".", "[", "]", "`", ";", "'", '"', "\\", '<', '>']
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            # randomly choose characters
            password_list = []

            for _ in range(1, 多少數字 + 1):
                password_list += random.choice(numbers)

            for _ in range(1, 多少符號 + 1):
                password_list += random.choice(symbols)

            for _ in range(1, 多少字母 + 1):
                password_list += random.choice(letters)


            # shuffle the password_list
            random.shuffle(password_list)

            # turn the password list into string
            password = ""
            for password_char in password_list:
                password += password_char

            has_lower_letter = False
            has_upper_letter = False
            has_number = False
            has_symbol = False
            has_length = False

            symbols = '`-=[]\\;\',./~!@#$%^&*()_+{}|:"<>?'

            for c in password:
                if c.islower():
                    has_lower_letter = True
                elif c.isupper():
                    has_upper_letter = True
                elif c.isnumeric():
                    has_number = True
                elif c in symbols:
                    has_symbol = True
                else:
                    return False

            if 6 <= len(password):
                has_length = True

            valid = all([
            has_lower_letter,
            has_upper_letter,
            has_number,
            has_symbol,
            has_length,
            ])

            embed=discord.Embed(title="Mahiro-BOT",description=f'<@{user_id}>', timestamp=datetime.now())
            embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
            if valid == True:
                valid = "🟢-合格"
                embed.color = 0x28FF28
            elif valid == False:
                valid = "🔴-不合格"
                embed.color = 0xAE0000

            embed.add_field(name = "密碼", value=f'||{password}||', inline=False)
            embed.add_field(name = "密碼強度", value=valid, inline=False)
            if has_lower_letter == False:
                embed.add_field(name = "", value="至少包含一個小寫字母", inline=False)
            if has_upper_letter == False:
                embed.add_field(name = "", value="至少包含一個大寫字母", inline=False)
            if has_number == False:
                embed.add_field(name = "", value="至少包含一個數字", inline=False)
            if has_symbol == False:
                embed.add_field(name = "", value="至少包含一個特殊符號", inline=False)
            if has_length == False:
                embed.add_field(name = "", value="至少長度要在6以上", inline=False)
            await ctx.respond(embed=embed,delete_after = 30)

def setup(bot):
    bot.add_cog(Password(bot))
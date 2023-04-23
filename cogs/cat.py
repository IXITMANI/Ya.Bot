import datetime

import disnake
import requests
from disnake.ext import commands


class PictureCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Показывает милого котика')
    async def cat(self, inter):
        a = requests.get('https://api.thecatapi.com/v1/images/search')
        data = a.json()
        embed = disnake.Embed(title="Милый котик Nya",
                              color=disnake.Color.random())
        embed.set_image(
            url=data[0]['url']
        )
        embed.set_author(
            name="Умнейший бот",
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )
        embed.set_footer(
            text=f"{datetime.datetime.now().date()}",
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )
        await inter.send(embed=embed)

    @commands.slash_command(description='Показывает милого пёсика')
    async def dog(self, inter):
        b = requests.get(' https://dog.ceo/api/breeds/image/random')
        data1 = b.json()
        embed = disnake.Embed(title="Милый пёсик Nya",
                              color=disnake.Color.random())
        embed.set_image(url=data1['message'])
        embed.set_author(
            name="Умнейший бот",
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )
        embed.set_footer(
            text=f"{datetime.datetime.now().date()}",
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )
        await inter.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(PictureCommand(bot))
import datetime

import disnake
import requests
from disnake.ext import commands


class ServerCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def server(self, inter):
        embed = disnake.Embed(
            color=disnake.Color.random()
        )
        if inter.guild.icon:
            embed.set_author(
                name=inter.guild.name,
                icon_url=inter.guild.icon.url,
            )
            embed.set_image(
                inter.guild.icon.url
            )
            embed.add_field(name=f'Колличество участников: {inter.guild.member_count}',
                            value="",
                            inline=False
                            )
            embed.set_footer(
                text=f"{datetime.datetime.now().date()}",
                icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
            )

            #     f"Название сервера {inter.guild.name}\nУчастников: {inter.guild.member_count}\n {inter.guild.icon.url}"
        else:
            embed.set_author(
                name=inter.guild.name,
                icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
            )
            embed.add_field(name=f'Колличество участников: {inter.guild.member_count}',
                            value="",
                            inline=False
                            )
            embed.set_footer(
                text=f"{datetime.datetime.now().date()}",
                icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
            )
        await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ServerCommand(bot))

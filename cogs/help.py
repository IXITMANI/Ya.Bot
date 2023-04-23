import datetime

import disnake
from disnake.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Помогает вам')
    async def help(self, inter):
        embed = disnake.Embed(title="Список команд",
                              color=disnake.Color.random())
        embed.add_field(
            name="/cat",
            value="Присылает милого котика",
            inline=False
        )
        embed.add_field(
            name="/dog",
            value="Присылает милого пёсика",
            inline=False
        )
        embed.add_field(
            name="/server",
            value="Данные о сервере",
            inline=False
        )
        embed.add_field(
            name="/question.py",
            value="Задай вопрос а бот на него ответит",
            inline=False
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


def setup(bot: commands.Bot):
    bot.add_cog(HelpCommand(bot))
import datetime

import disnake
import openai
from disnake.ext import commands


class QuestionCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='бот отвечает на любой вопрос')
    async def question(self, inter, вопрос: str):
        prom = вопрос
        await inter.response.defer()
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=[
                                                      {"role": "user",
                                                       "content": f"{prom}"}
                                                  ])

        embed = disnake.Embed(title=prom.capitalize(), description=f"{completion.choices[0].message.content}",
                              color=disnake.Color.green())
        embed.set_author(
            name="Умнейший бот",
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )
        embed.set_footer(
            text=f"{datetime.datetime.now().date()}",
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )
        await inter.followup.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(QuestionCommand(bot))

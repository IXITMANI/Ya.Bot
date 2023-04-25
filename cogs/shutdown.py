import datetime

import disnake
import sys
from disnake.ext import commands


class ShutdownCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='ShutdownCommand')
    async def shutdown(self, inter, password: str):
        if password == '123451':
            await inter.send('Бот успешно оффнулся')
            sys.exit()
        else:
            await inter.send('Сам shutdown')


def setup(bot: commands.Bot):
    bot.add_cog(ShutdownCommand(bot))
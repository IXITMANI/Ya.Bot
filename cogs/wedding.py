import disnake
import sqlite3
from disnake.ext import commands

con = sqlite3.connect("db\married.sqlite")
cur = con.cursor()


class WeddingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.num = len(cur.execute("""SELECT * FROM married""").fetchall())

    @commands.slash_command(description='брачный договор')
    async def wedding(self, inter, husband: str, wife: str):
        if len(cur.execute(f"""
                            SELECT * from married WHERE husband = '{husband}'
                            """).fetchall()) > 0:
            await inter.response.send_message(f'Пользователь {husband} уже женат')
        elif len(cur.execute(f"""
                            SELECT * from married WHERE wife = '{wife}'
                            """).fetchall()) > 0:
            await inter.response.send_message(f'Пользователь {wife} уже замужем')
        else:
            cur.execute(f"""INSERT INTO married(id,husband, wife, date)
                    VALUES({self.num + 1}, '{husband}', '{wife}', '123')""")
            self.num += 1
            con.commit()
            await inter.response.send_message('Все из гуд')


def setup(bot: commands.Bot):
    bot.add_cog(WeddingCommand(bot))

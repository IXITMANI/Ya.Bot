import datetime
import sqlite3
import disnake
from disnake.ext import commands

con = sqlite3.connect("db\married.sqlite")
cur = con.cursor()

class MarriageCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.husband = None
        self.wife = None
        self.num = cur.execute("""SELECT * FROM married""").fetchall()[-1][0]

    def check(self, user: disnake.ApplicationCommandInteraction.author):
        res = cur.execute(f"""
                                    SELECT * from married WHERE husband = '{user.mention}' OR wife = '{user.mention}'
                                    """).fetchall()
        if len(res) == 0:
            return None
        elif res[0][1] == user.mention:
            return f'''Пользователь {user.mention} уже в браке с {res[0][2]}'''
        else:
            return f'''Пользователь {user.mention} уже в браке с {res[0][1]}'''

    @commands.slash_command()
    async def marriage(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        ans = self.check(inter.author)
        if ans:
            await inter.send(ans)
            return
        ans = self.check(member)
        if ans:
            await inter.send(ans)
            return

        self.husband = inter.author
        self.wife = member
        await inter.response.send_message(
            f"{member.mention}, вы хотите выйти замуж за {inter.author.mention}?",
            components=[
                disnake.ui.Button(label="Yes", style=disnake.ButtonStyle.success, custom_id="yes"),
                disnake.ui.Button(label="No", style=disnake.ButtonStyle.danger, custom_id="no"),
            ],
        )

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.author != self.wife:
            await inter.send(f'Только {self.wife.mention} может отвечать на предложение')
            return
        if inter.component.custom_id not in ["yes", "no"]:
            return

        await inter.message.delete()

        if inter.component.custom_id == "yes":
            await inter.send(f"{inter.author.mention} вышла замуж за {self.husband.mention}")
            cur.execute(f"""INSERT INTO married(id,husband, wife, date)
                               VALUES({self.num + 1}, '{self.husband.mention}', '{self.wife.mention}', '{datetime.datetime.now().date()}')""")
            self.num += 1
            con.commit()

        elif inter.component.custom_id == "no":
            await inter.send(f"{self.husband.mention} получил отказ от {self.wife.mention}")
        self.husband = None
        self.wife = None

    @commands.slash_command(description='расторжение брака')
    async def divorce (self, inter: disnake.ApplicationCommandInteraction):
        ans = self.check(inter.author)
        if not ans:
            await inter.send(f'''Вы не состоите в браке''')
        else:
            cur.execute(f"""DELETE FROM married WHERE husband = '{inter.author.mention}' OR wife = '{inter.author.mention}'""")

    @commands.slash_command(description='вывести все браки')
    async def marriage_info(self, inter: disnake.ApplicationCommandInteraction):
        ans = ''
        resp = cur.execute(f"""SELECT * from married""").fetchall()
        for el in resp:
            ans += f'Муж: {el[1]}, Жена: {el[2]}, Зарегистрирован: {el[3]}\n'
        await inter.send(ans)

    @commands.slash_command(description='Инфа по твоему браку')
    async def my_marriage(self, inter: disnake.ApplicationCommandInteraction):
        user = inter.author
        res = cur.execute(f"""
                                            SELECT * from married WHERE husband = '{user.mention}' OR wife = '{user.mention}'
                                            """).fetchall()
        if len(res) == 0:
            await inter.send('Вы не состоите в браке')
        elif res[0][1] == user.mention:
            await inter.send(f'''Вы находитесь в браке с {res[0][2]}''')
        else:
            await inter.send(f'''Вы находитесь в браке с {res[0][1]}''')

    @commands.slash_command(description='Инфа по твоему браку')
    async def my_marriage(self, inter: disnake.ApplicationCommandInteraction):
        user = inter.author
        res = cur.execute(f"""
                                                SELECT * from married WHERE husband = '{user.mention}' OR wife = '{user.mention}'
                                                """).fetchall()
        if len(res) == 0:
            await inter.send('Вы не состоите в браке')
        elif res[0][1] == user.mention:
            await inter.send(f'''Вы находитесь в браке с {res[0][2]}''')
        else:
            await inter.send(f'''Вы находитесь в браке с {res[0][1]}''')

    @commands.slash_command(description='Инфа по браку юзера')
    async def check_marriage(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        res = cur.execute(f"""
                                            SELECT * from married WHERE husband = '{member.mention}' OR wife = '{member.mention}'
                                            """).fetchall()
        if len(res) == 0:
            await inter.send(f'''Этот пользователь не состоит в браке''')
        elif res[0][1] == member.mention:
            await inter.send(f'''Пользователь {member.mention} в браке с {res[0][2]}''')
        else:
            await inter.send(f'''Пользователь {member.mention} в браке с {res[0][1]}''')

def setup(bot: commands.Bot):
    bot.add_cog(MarriageCommand(bot))
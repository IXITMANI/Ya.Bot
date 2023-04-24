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
        self.a_url = None
        if len(cur.execute("""SELECT * FROM married""").fetchall()) == 0:
            self.num = 0
        else:
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
        self.a_url = inter.author.display_avatar.url
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
        embed = disnake.Embed(title=f"Предлагает вам вступить в брак",
                              color=disnake.Color.random())
        embed.set_author(name=str(self.husband)[:-5], icon_url=inter.author.display_avatar.url)
        await inter.send(
            f'||{member.mention}||',
            embed=embed,
            components=[
                disnake.ui.Button(label="Да", style=disnake.ButtonStyle.success, custom_id="yes"),
                disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.danger, custom_id="no"),
            ], delete_after=30
        )

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.author != self.wife:
            await inter.send(f'Только {self.wife.mention} может отвечать на предложение', ephemeral=True)
            return
        if inter.component.custom_id not in ["yes", "no"]:
            return

        await inter.message.delete()

        if inter.component.custom_id == "yes":
            embed = disnake.Embed(title=f"Теперь в браке с {str(self.wife)[:-5]}",
                                  color=disnake.Color.random())
            embed.set_author(name=str(self.husband)[:-5], icon_url=self.a_url)
            await inter.send(embed=embed, delete_after=7)
            cur.execute(f"""INSERT INTO married(id,husband, wife, date)
                               VALUES({self.num + 1}, '{self.husband.mention}', '{self.wife.mention}', '{datetime.datetime.now().date()}')""")
            self.num += 1
            con.commit()

        elif inter.component.custom_id == "no":
            embed = disnake.Embed(title=f"Получил отказ от {str(self.wife)[:-5]}",
                                  color=disnake.Color.random())
            embed.set_author(name=str(self.husband)[:-5], icon_url=self.a_url)
            await inter.send(embed=embed, delete_after=7)
        self.husband = None
        self.wife = None

    @commands.slash_command(description='расторжение брака')
    async def divorce(self, inter: disnake.ApplicationCommandInteraction):
        ans = self.check(inter.author)
        if not ans:
            embed = disnake.Embed(title=f"Вы холостяк",
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)
        else:
            embed = disnake.Embed(title=f"Брак успешно расторгнут",
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            cur.execute(
                f"""DELETE FROM married WHERE husband = '{inter.author.mention}' OR wife = '{inter.author.mention}'""")
            await inter.send(embed=embed, delete_after=7)

    @commands.slash_command(description='вывести все браки')
    async def marriage_info(self, inter: disnake.ApplicationCommandInteraction):
        ans = ''
        resp = cur.execute(f"""SELECT * from married""").fetchall()
        embed = disnake.Embed(title=f"Список всех браков:",
                              color=disnake.Color.random())
        embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
        for el in resp:
            embed.add_field(name=f'Муж: {el[1]}, Жена: {el[2]}, Зарегистрирован: {el[3]}', value="", inline=False)
        await inter.send(embed=embed, delete_after=60)

    @commands.slash_command(description='Инфа по твоему браку')  # Решу завтра
    async def my_marriage(self, inter: disnake.ApplicationCommandInteraction):
        user = inter.author
        res = cur.execute(f"""
                                            SELECT * from married WHERE husband = '{user.mention}' OR wife = '{user.mention}'
                                            """).fetchall()
        print(res)
        if len(res) == 0:
            embed = disnake.Embed(title=f"Вы холостяк",
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)
        elif res[0][1] == user.mention:
            embed = disnake.Embed(title=f'Вы находитесь в браке с {res[0][2]}',  # Решу завтра
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)
        else:
            embed = disnake.Embed(title=f'Вы находитесь в браке с {res[0][1]}',  # Решу завтра
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)


def setup(bot: commands.Bot):
    bot.add_cog(MarriageCommand(bot))

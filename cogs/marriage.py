import datetime
import sqlite3
import disnake
from disnake.ext import commands

con = sqlite3.connect("db\married.sqlite")
cur = con.cursor()


class MarriageCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.husband: disnake.Member = None
        self.wife: disnake.Member = None
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
            return f'''Пользователь {user.display_name} уже в браке с {res[0][2]}'''
        else:
            return f'''Пользователь {user.display_name} уже в браке с {res[0][1]}'''

    @commands.slash_command()
    async def marriage(self, inter: disnake.ApplicationCommandInteraction, жена: disnake.Member):
        member = жена
        if inter.author == member:
            embed = disnake.Embed(title=f"Нельзя самому с собой же в брак вступить",
                                  color=disnake.Color.random())
            embed.set_author(name=str(self.husband)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, ephemeral=True)
        else:
            self.a_url = inter.author.display_avatar.url
            ans = self.check(inter.author)
            if ans:
                embed = disnake.Embed(title=f"{ans}",
                                      color=disnake.Color.random())
                embed.set_author(name=str(self.husband)[:-5], icon_url=inter.author.display_avatar.url)
                await inter.send(embed=embed, delete_after=7, ephemeral=True)
                return
            ans = self.check(member)
            if ans:
                embed = disnake.Embed(title=f"{ans}",
                                      color=disnake.Color.random())
                embed.set_author(name=str(self.husband)[:-5], icon_url=inter.author.display_avatar.url)
                await inter.send(embed=embed, delete_after=7, ephemeral=True)
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
            embed = disnake.Embed(title=f"Теперь в браке с {self.wife.display_name}",
                                  color=disnake.Color.random())
            embed.set_author(name=self.husband.display_name, icon_url=self.a_url)
            await inter.author.add_roles(inter.guild.get_role(1100088795652702218))
            await self.husband.add_roles(inter.guild.get_role(1100092860210090054))
            await inter.send(embed=embed, delete_after=7)
            cur.execute(f"""INSERT INTO married(id,husband, wife, date)
                               VALUES({self.num + 1}, '{self.husband.mention}', '{self.wife.mention}', '{datetime.datetime.now().date()}')""")
            self.num += 1
            con.commit()

        elif inter.component.custom_id == "no":
            embed = disnake.Embed(title=f"Получил отказ от {self.wife.display_name}",
                                  color=disnake.Color.random())
            embed.set_author(name=self.husband.display_name, icon_url=self.a_url)
            await inter.send(embed=embed, delete_after=7)
        self.husband = None
        self.wife = None

    @commands.slash_command(description='расторжение брака')
    async def divorce(self, inter: disnake.ApplicationCommandInteraction):
        ans = self.check(inter.author)
        res = cur.execute(f"""
                                                    SELECT * from married WHERE husband = '{inter.author.mention}' OR wife = '{inter.author.mention}'
                                                    """).fetchall()
        if not ans:
            embed = disnake.Embed(title=f"Вы холостяк",
                                  color=disnake.Color.random())
            embed.set_author(name=inter.author.display_name, icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)
        else:
            self.wife = inter.guild.get_member(int(res[0][2][2:-1]))
            self.husband = inter.guild.get_member(int(res[0][1][2:-1]))
            await self.husband.remove_roles(inter.guild.get_role(1100092860210090054))
            await self.wife.remove_roles(inter.guild.get_role(1100088795652702218))
            # await self.wife.remove_roles(inter.guild.get_role(1100092860210090054))
            embed = disnake.Embed(title=f"Брак успешно расторгнут",
                                  color=disnake.Color.random())
            embed.set_author(name=inter.author.display_name, icon_url=inter.author.display_avatar.url)
            cur.execute(
                f"""DELETE FROM married WHERE husband = '{inter.author.mention}' OR wife = '{inter.author.mention}'""")
            await inter.send(embed=embed, delete_after=7)

    @commands.slash_command(description='Выводит список всех браков')
    async def marriage_info(self, inter: disnake.ApplicationCommandInteraction):
        ans = ''
        resp = cur.execute(f"""SELECT * from married""").fetchall()
        embed = disnake.Embed(title=f"Список всех браков:",
                              color=disnake.Color.random())
        embed.set_author(name=inter.author.display_name, icon_url=inter.author.display_avatar.url)
        for el in resp:
            embed.add_field(
                name=f'Муж: {inter.guild.get_member(int(el[1][2:-1]))}, Жена: {inter.guild.get_member(int(el[2][2:-1]))}, Зарегистрирован: {el[3]}',
                value="", inline=False)
        await inter.send(embed=embed, delete_after=60)

    @commands.slash_command(description='Инфа по твоему браку')  # Решу завтра
    async def my_marriage(self, inter: disnake.ApplicationCommandInteraction):
        user: disnake.Member = inter.author
        res = cur.execute(f"""
                                            SELECT * from married WHERE husband = '{user.mention}' OR wife = '{user.mention}'
                                            """).fetchall()
        if len(res) == 0:
            embed = disnake.Embed(title=f"Вы холостяк",
                                  color=disnake.Color.random())
            embed.set_author(name=inter.author.display_name, icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)
        elif res[0][1] == user.mention:
            self.wife = inter.guild.get_member(int(res[0][2][2:-1]))
            embed = disnake.Embed(title=f'Вы находитесь в браке с {self.wife.display_name}',
                                  color=disnake.Color.random())
            embed.set_author(name=inter.author.display_name, icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)
        else:
            self.husband = inter.guild.get_member(int(res[0][1][2:-1]))
            embed = disnake.Embed(title=f'Вы находитесь в браке с {self.husband.display_name}',
                                  color=disnake.Color.random())
            embed.set_author(name=inter.author.display_name, icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)

    @commands.slash_command(description='Информация по браку юзера')
    async def check_marriage(self, inter: disnake.ApplicationCommandInteraction,
                             любовник_или_любовница: disnake.Member):
        member = любовник_или_любовница
        res = cur.execute(f"""
                                            SELECT * from married WHERE husband = '{member.mention}' OR wife = '{member.mention}'
                                            """).fetchall()
        if len(res) == 0:
            embed = disnake.Embed(title=f"Холостяк",
                                  color=disnake.Color.random())
            embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)
        elif res[0][1] == member.mention:
            self.wife = inter.guild.get_member(int(res[0][2][2:-1]))
            self.husband = inter.guild.get_member(int(res[0][1][2:-1]))
            embed = disnake.Embed(title=f'В браке с {self.wife.display_name}',
                                  color=disnake.Color.random())
            embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)
        else:
            self.wife = inter.guild.get_member(int(res[0][2][2:-1]))
            self.husband = inter.guild.get_member(int(res[0][1][2:-1]))
            embed = disnake.Embed(title=f'В браке с {self.husband.display_name}',
                                  color=disnake.Color.random())
            embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
            await inter.send(embed=embed, delete_after=7)


def setup(bot: commands.Bot):
    bot.add_cog(MarriageCommand(bot))

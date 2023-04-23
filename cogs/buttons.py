import disnake
from disnake.ext import commands


class ButtonsCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.husband = None
        self.wife = None

    @commands.slash_command()
    async def buttons(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
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
            return
        if inter.component.custom_id not in ["yes", "no"]:
            return
        await inter.message.delete()
        if inter.component.custom_id == "yes":
            await inter.send(f"{inter.author.mention} вышла замуж за {self.husband.mention}")
        elif inter.component.custom_id == "no":
            await inter.send("Если нажата нет")

def setup(bot: commands.Bot):
    bot.add_cog(ButtonsCommand(bot))
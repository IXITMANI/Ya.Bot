import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all(),
                   activity=disnake.Game('попе пальчиком', status=disnake.Status.online))

bot.remove_command('help')


@bot.event
async def on_ready():
    print('Всё хорошо')


@bot.slash_command(description='Помогает вам')
async def help(inter):
    msg = "Привет"
    await inter.response.send_message(msg)


@bot.slash_command()
async def server(inter):
    await inter.response.send_message(
        f"Название сервера {inter.guild.name}\nУчастников: {inter.guild.member_count}"
    )


@bot.slash_command()
async def test(inter):
    embed = disnake.Embed(title="Title", description="description", url="https://yandex.ru",
                          color=disnake.Color.dark_blue())
    await inter.send(embed=embed)


token = ''
tmp = open('token', 'r').readline()
for item in tmp:
    token += chr(ord(item) - 5)
bot.run(token)

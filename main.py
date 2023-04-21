import disnake
from disnake.ext import commands
import youtube_dl

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())

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


@bot.slash_command()
async def question(inter, prom: str):
    tok = 100000
    await inter.response.defer()
    completion = openai.Completion.create(engine="text-davinci-003",
                                          prompt=prom,
                                          temperature=0.5,
                                          max_tokens=min(4000 - len(prom), tok))
    embed = disnake.Embed(title="Ответ", description=f"{completion.choices[0]['text']}",
                          color=disnake.Color.green())
    print(completion.choices[0]['text'])
    await inter.followup.send(embed=embed)


@bot.slash_command()
async def play(inter):
    ...

token = ''
tmp = open('token', 'r').readline()
for item in tmp:
    token += chr(ord(item) - 5)
bot.run(token)

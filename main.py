import disnake
import requests
from disnake.ext import commands
import openai

temp = open('token', 'r').readlines()[1]
openai.api_key = temp
bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all(),
                   activity=disnake.Game('попе пальчиком', status=disnake.Status.online))

bot.remove_command('help')


@bot.event
async def on_ready():
    print('Всё хорошо')


@bot.slash_command(description='Помогает вам')
async def help(inter):
    msg = "Привет, я чем то помогаю вам"
    await inter.response.send_message(msg)


@bot.slash_command(description='Показывает милого котика')
async def cat(inter):
    a = requests.get('https://api.thecatapi.com/v1/images/search')
    data = a.json()
    embed = disnake.Embed(title="Милый котик Nya",
                          color=disnake.Color.random())
    embed.set_image(url=data[0]['url'])
    embed.set_author(
        name="Умнейший бот",
        icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
    )
    await inter.send(embed=embed)


@bot.slash_command(description='Показывает милого пёсика')
async def dog(inter):
    b = requests.get(' https://dog.ceo/api/breeds/image/random')
    data1 = b.json()
    embed = disnake.Embed(title="Милый пёсик Nya",
                          color=disnake.Color.random())
    embed.set_image(url=data1['message'])
    embed.set_author(
        name="Умнейший бот",
        icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
    )
    await inter.send(embed=embed)


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


@bot.slash_command(description='бот отвечает на любой вопрос')
async def question(inter, вопрос: str):
    prom = вопрос
    await inter.response.defer()
    completion = openai.Completion.create(engine="text-davinci-003",
                                          prompt=prom,
                                          temperature=0.5,
                                          max_tokens=1_000)

    embed = disnake.Embed(title="Ответ", description=f"{completion.choices[0]['text']}",
                          color=disnake.Color.green())
    embed.set_author(
        name="Умнейший бот",
        icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
    )
    await inter.followup.send(embed=embed)


token = ''
tmp = open('token', 'r').readlines()[0]
for item in tmp:
    token += chr(ord(item) - 5)
token = token[:-1]
bot.run(token)

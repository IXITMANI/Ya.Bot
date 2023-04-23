import disnake
import requests
from disnake.ext import commands
import openai
import datetime

temp = open('token', 'r').readlines()[1]
openai.api_key = temp
bot = commands.Bot(
    command_prefix='!', intents=disnake.Intents.all(),
    activity=disnake.Game('PyCharm', status=disnake.Status.dnd)
)

bot.remove_command('help')


@bot.event
async def on_ready():
    print('Всё хорошо')


@bot.slash_command(description='Помогает вам')
async def help(inter):
    embed = disnake.Embed(title="Список команд",
                          color=disnake.Color.random())
    embed.add_field(
        name="/cat",
        value="Присылает милого котика",
        inline=False
    )
    embed.add_field(
        name="/dog",
        value="Присылает милого пёсика",
        inline=False
    )
    embed.add_field(
        name="/server",
        value="Данные о сервере",
        inline=False
    )
    embed.add_field(
        name="/question",
        value="Задай вопрос а бот на него ответит",
        inline=False
    )
    embed.set_author(
        name="Умнейший бот",
        icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
    )
    embed.set_footer(
        text=f"{datetime.datetime.now().date()}",
        icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
    )
    await inter.send(embed=embed)


@bot.slash_command(description='Показывает милого котика')
async def cat(inter):
    a = requests.get('https://api.thecatapi.com/v1/images/search')
    data = a.json()
    embed = disnake.Embed(title="Милый котик Nya",
                          color=disnake.Color.random())
    embed.set_image(
        url=data[0]['url']
    )
    embed.set_author(
        name="Умнейший бот",
        icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
    )
    embed.set_footer(
        text=f"{datetime.datetime.now().date()}",
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
    embed.set_footer(
        text=f"{datetime.datetime.now().date()}",
        icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
    )
    await inter.send(embed=embed)


@bot.slash_command()
async def server(inter):
    embed = disnake.Embed(
        color=disnake.Color.random()
    )
    if inter.guild.icon:
        embed.set_author(
            name=inter.guild.name,
            icon_url=inter.guild.icon.url,
        )
        embed.set_image(
            inter.guild.icon.url
        )
        embed.add_field(name=f'Колличество участников: {inter.guild.member_count}',
                        value="",
                        inline=False
                        )
        embed.set_footer(
            text=f"{datetime.datetime.now().date()}",
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )

        #     f"Название сервера {inter.guild.name}\nУчастников: {inter.guild.member_count}\n {inter.guild.icon.url}"
    else:
        embed.set_author(
            name=inter.guild.name,
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )
        embed.add_field(name=f'Колличество участников: {inter.guild.member_count}',
                        value="",
                        inline=False
                        )
        embed.set_footer(
            text=f"{datetime.datetime.now().date()}",
            icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
        )
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
    embed.set_footer(
        text=f"{datetime.datetime.now().date()}",
        icon_url="https://avatars.mds.yandex.net/i?id=d0bb10ef328847ecd137d5813a022aad14eafa96-5714527-images-thumbs&ref=rim&n=33&w=150&h=150",
    )
    await inter.followup.send(embed=embed)


token = ''
tmp = open('token', 'r').readlines()[0]
for item in tmp:
    token += chr(ord(item) - 5)
token = token[:-1]
bot.run(token)

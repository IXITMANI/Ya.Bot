import datetime

import disnake
import requests
from disnake.ext import commands
import openai

tk = ""
temp_1 = open('token', 'r').readlines()[1][:-1]
for item in temp_1:
    tk += chr(ord(item) - 5)
tk = tk[:-1]
openai.api_key = tk
bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())
bot.load_extensions('cogs')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n"
          f"Кароче всё робит")


token=""
tmp = open('token', 'r').readlines()[0]
for item in tmp:
    token += chr(ord(item) - 5)
token = token[:-1]
bot.run(token)

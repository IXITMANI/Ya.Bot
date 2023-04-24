import datetime

import disnake
import requests
from disnake.ext import commands
import openai

openai.api_key = open('token', 'r').readlines()[1]
bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())
bot.load_extensions('cogs')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\nКароче всё робит")


token = ""
tmp = open('token', 'r').readlines()[0]
for item in tmp:
    token += chr(ord(item) - 5)
token = token[:-1]
bot.run(token)

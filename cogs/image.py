import disnake
from disnake.ext import commands
import os


class ImageCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Сохраняет картинку')
    async def save(self, inter, name: str, file: disnake.Attachment):
        num = len([f for f in os.listdir('images')
                   if os.path.isfile(os.path.join('images', f))])
        if num >= 20:
            embed = disnake.Embed(title=f'Сохранить не удалось, картинок уже слишком много',
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed)
        else:
            embed = disnake.Embed(title=f'Картинка {name}.png успешно сохранена\n{num + 1}/20 картинок загружено',
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await file.save(f'images\{name}.png')
            await inter.send(embed=embed)

    @commands.slash_command(description='Отправить картинку')
    async def photo(self, inter, name: str):
        await inter.response.defer()
        if os.path.exists(f'images\{name}.png'):
            embed = disnake.Embed(title=f'{name}',
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            embed.set_image(f'images\{name}.png')
            await inter.followup.send(file=disnake.File(f'images\{name}.png'))
        else:
            embed = disnake.Embed(title='Картинки с указанным именем не существует!',
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed)

    @commands.slash_command(description='Список всех картинок')
    async def allpic(self, inter):
        embed = disnake.Embed(title='Картинки с указанным именем не существует!',
                              color=disnake.Color.random())
        embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
        for f in os.listdir('images'):
            if os.path.isfile:
                f = os.path.join('images', f)[:-4]

        await inter.send(embed=embed)

    @commands.slash_command(description='удалить картинку')
    async def delete(self, inter, name: str):
        if os.path.exists(f'images\{name}.png'):
            os.remove(f'images\{name}.png')
            embed = disnake.Embed(title=f"Картинка {name} успешно удалена.",
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed)
        else:
            embed = disnake.Embed(title=f"Картинки {name} не существует.",
                                  color=disnake.Color.random())
            embed.set_author(name=str(inter.author)[:-5], icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ImageCommand(bot))

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
            await inter.send('Сохранить не удалось, картинок уже слишком много')
        else:
            await file.save(f'images\{name}.png')
            await inter.send(f'Картинка {name}.png успешно сохранена\n'
                             f'{num + 1}/20 картинок загружено')

    @commands.slash_command(description='Отправить картинку')
    async def photo(self, inter, name: str):
        await inter.response.defer()
        if os.path.exists(f'images\{name}.png'):
            await inter.followup.send(file=disnake.File(f'images\{name}.png'))
        else:
            await inter.send('картинки с указанным именем не существует!')

    @commands.slash_command(description='все картинки')
    async def allpic(self, inter):
        a = [f[:-4] for f in os.listdir('images')
                   if os.path.isfile(os.path.join('images', f))]
        await inter.send('\n'.join(a))

    @commands.slash_command(description='удалить картинку')
    async def delete(self, inter, name: str):
        if os.path.exists(f'images\{name}.png'):
            os.remove(f'images\{name}.png')
            await inter.send(f"Картинка {name} успешно удалена.")
        else:
            await inter.send(f"Картинки {name} не существует.")


def setup(bot: commands.Bot):
    bot.add_cog(ImageCommand(bot))
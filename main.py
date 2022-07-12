from random import random

import discord  # Подключаем библиотеку
from discord.ext import commands
from Database.Database import UserHandler
from constants import token

# Задаём префикс и интенты
bot = commands.Bot(command_prefix='>')


@bot.event
async def on_ready():
    users = UserHandler()
    for member in bot.get_all_members():
        if not users.check_user(member.id):
            users.add_user(member.id)

    print("Бот запущен")


# С помощью декоратора создаём первую команду
@bot.command()
async def profile(ctx):
    users = UserHandler()
    if not users.check_user(ctx.author.id):
        users.add_user(ctx.author.id)
        await ctx.send(f'{ctx.author.display_name} о тебе еще нет данных')
    else:
        stat = users.get_profile(ctx.author.id)
        if stat[0]+stat[1] == 0:
            await ctx.send(f'{ctx.author.display_name} о тебе еще нет данных')
        else:
            await ctx.send(f'{ctx.author.display_name} побед {stat[0]} ({stat[0]/(stat[0]+stat[1])*100}%) поражений {stat[1]}')


@bot.command()
async def stats(ctx):
    users = UserHandler()
    if not users.check_user(ctx.author.id):
        users.add_user(ctx.author.id)
        await ctx.send(f'{ctx.author.display_name} о тебе еще нет данных')
    else:
        stat = users.get_profile(ctx.author.id)
        await ctx.send(f'побед {stat[0]}  поражений {stat[1]}')


@bot.command()
async def game(ctx):
    users = UserHandler()
    if not users.check_user(ctx.author.id):
        users.add_user(ctx.author.id)
    if random() > 0.33:
        users.get_game(ctx.author.id, 0)
        await ctx.send('поражение')
    else:
        users.get_game(ctx.author.id, 1)
        await ctx.send('победа')

bot.run(token)

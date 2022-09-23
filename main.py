from random import random
from datetime import datetime
from discord.ext import tasks
import discord  # Подключаем библиотеку
from discord.ext import commands
from Database.Database import ServerHandler
from constants import TOKEN

intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix='Шиза ', intents=intent)

last_day = None


@bot.event
async def on_ready():
    srv = ServerHandler()
    for guild in bot.guilds:
        srv.add_server(guild.id, guild.name)

    DalyCard.start()
    print("Бот запущен")


@tasks.loop(hours=2)
async def DalyCard():
    if 10 <= datetime.now().hour <= 22:
        srv = ServerHandler()
        for i in srv.get_servers():
            if i.last_day != str(datetime.now().day):
                channels = bot.get_guild(i.discord_id).text_channels
                for channel in channels:
                    if channel.id == i.daly_channel:
                        match datetime.weekday(datetime.now()):
                            case 0:
                                await channel.send(file=discord.File('resources/monday.jpg'))
                            case 1:
                                await channel.send(file=discord.File('resources/tuesday.jpg'))
                            case 2:
                                await channel.send(file=discord.File('resources/wednesday.jpg'))
                            case 3:
                                await channel.send(file=discord.File('resources/thursday.jpg'))
                            case 4:
                                await channel.send(file=discord.File('resources/friday.jpg'))
                            case 5:
                                await channel.send(file=discord.File('resources/saturday.jpg'))
                            case 6:
                                await channel.send(file=discord.File('resources/sunday.jpg'))
                        srv.set_day(i.discord_id, str(datetime.now().day))


@bot.command()
async def set_daly_channel(ctx):
    srv = ServerHandler()
    srv.set_daly_channel(ctx.guild.id, ctx.message.channel.id)
    await ctx.send("Канал установлен")

bot.run(TOKEN)

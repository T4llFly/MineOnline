import discord
from discord.ext import commands
import asyncio
from mcstatus import JavaServer

TOKEN = input("Введите свой токен: ")
SERVER_IP = input("Введите IP сервера: ")
SERVER_PORT = input("Введите порт сервера (стандарт 25565): ")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
server = JavaServer.lookup(f'{SERVER_IP}:{SERVER_PORT}')

@bot.event
async def on_ready():
    print(f'Запущен как {bot.user}')
    bot.loop.create_task(update_presence())
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)

async def update_presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            status = server.status()
            await bot.change_presence(activity=discord.Game(name=f"{status.players.online} игроков онлайн"))
        except:
            await bot.change_presence(activity=discord.Game(name="Тех.обслуживание"))
        await asyncio.sleep(30)

@bot.tree.command(name="online")
async def online(interaction: discord.Interaction):
        try:
            status = server.status()
            players = "\n".join([player.name for player in status.players.sample])
            online = status.players.online
            max_players = status.players.max
            response = f"**Сейчас на сервере {online}/{max_players} игроков:**\n{players}"
        except:
            response = "**Сервер на тех.обслуживании**"
        await interaction.response.send_message(response)

bot.run(TOKEN)
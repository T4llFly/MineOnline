import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from mcstatus import JavaServer

TOKEN = input("Введите свой токен: ")
SERVER_IP = None
SERVER_PORT = 25565

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
            await bot.change_presence(activity=discord.Game(name=f"{status.players.online}/{status.players.max} игроков онлайн"))
        except:
            await bot.change_presence(activity=discord.Game(name="Введите IP и порт сервера"))
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
            response = "**Сейчас игроков нет**"
        await interaction.response.send_message(response)

@bot.tree.command(name="ip", description="Добавление IP адреса сервера")
@app_commands.describe(ip = "IP адрес сервера")
async def ip(interaction: discord.Interaction, ip: str):
    global SERVER_IP
    SERVER_IP = ip
    await interaction.response.send_message(f"Теперь указан IP: **{ip}**")

    global server
    server = JavaServer.lookup(f'{SERVER_IP}:{SERVER_PORT}')

@bot.tree.command(name="port", description="Добавление порта сервера")
@app_commands.describe(port = "Порт сервера")
async def port(interaction: discord.Interaction, port: int):
    global SERVER_PORT
    SERVER_PORT = port
    await interaction.response.send_message(f"Теперь указан порт: **{port}**")

    global server
    server = JavaServer.lookup(f'{SERVER_IP}:{SERVER_PORT}')

bot.run(TOKEN)
import discord
import asyncio
from mcstatus import JavaServer

TOKEN = input("Введите свой токен: ")
SERVER_IP = input("Введите IP сервера: ")
SERVER_PORT = input("Введите порт сервера (стандарт 25565): ")

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'Запущен как {client.user}')
    client.loop.create_task(update_presence())

async def update_presence():
    await client.wait_until_ready()
    server = JavaServer.lookup(f'{SERVER_IP}:{SERVER_PORT}')
    while not client.is_closed():
        try:
            status = server.status()
            await client.change_presence(activity=discord.Game(name=f"{status.players.online} игроков онлайн"))
        except:
            await client.change_presence(activity=discord.Game(name="Тех.обслуживание"))
        await asyncio.sleep(30)

client.run(TOKEN)
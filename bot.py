import discord

from dotenv import load_dotenv
import os
load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged as in {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "yama":
        await message.channel.send('Pato do marcelinho')

client.run(os.getenv('TOKEN'))

import discord
from discord.ext import commands
from dotenv import load_dotenv
from forex_python.converter import CurrencyRates
import os
import random
load_dotenv()

# client = discord.Client()
client = commands.Bot(command_prefix='.')

amiguinhos= {
    'marcelo':'o mais brabo',
    'pedrao':'god demais',
    'lucio':'estrelinha',
    'yama':'meu patinho',
    'nick': 'argh',
    'fuka':'vc acha o fuka ruim?',
    'eiki':'cingarro da kanser',
    'amanda':'challenger no lol',
    'sulley':'deus de modcom',
    'sophia':'pitanguinha <3',
    'bilbs': 'namora cmg tbm hehe'
}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,activity=discord.Game("o yama no mar"))
    print("We have logged as in {0.user}".format(client))

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
async def msg(ctx, *, question):
    if question.lower() == client.user:
        return

    # Retorna a característica do amiguinho
    for i,v in amiguinhos.items():
        if question.lower() == i:
            await ctx.send(f"{i}, {v}")

    # listinha de amigos disponivel
    if question.lower() == "lista":
        lista_amigos = []
        for i,v in amiguinhos.items():
            lista_amigos.append(i)
        await ctx.send(' | '.join(lista_amigos))
    # Digitou errado
    else:
        await ctx.send("Opa, ese comando n existe.\ndigite '.msg lista' para saber a lista de amiguinhos que vc pode usar")
    
@client.command(description="joins a voice channel")
async def join(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send('Entre num canal para usar esse comando!')

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client

@client.command(description="stops and disconnects the bot from voice")
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("I'm not in a voice channel, use the join command to make me join")
    else:
        await ctx.voice_client.disconnect()
        await ctx.send('Bot left')

@client.command(aliases=['paly', 'queue', 'que'])
async def play(ctx):
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio('./audios/so2.mp3')
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)



client.run(os.getenv('TOKEN'))

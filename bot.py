import discord
from discord.ext import commands
from dotenv import load_dotenv
from forex_python.converter import CurrencyRates
import os
import random
import youtube_dl
import time
load_dotenv()

# client = discord.Client()
client = commands.Bot(command_prefix='.')
intents = discord.Intents().all()
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
    'bilbs': 'namora cmg hehe'
}

lista_audios=[]
for filename in os.listdir('./audios'):
    lista_audios.append(filename)



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
            return

    # listinha de amigos disponivel
    if question.lower() == "lista":
        lista_amigos = []
        for i,v in amiguinhos.items():
            lista_amigos.append(i)
        await ctx.send(' | '.join(lista_amigos))
    # Digitou errado
    else:
        await ctx.send("Opa, ese comando n existe.\ndigite '.msg lista' para saber a lista de amiguinhos que vc pode usar")

@client.command(aliases=['paly', 'queue', 'que'])
async def audio(ctx, *, question):
        # FAZ ELE ENTRAR NA CALL
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send('Entre num canal para usar esse comando!')

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client
    # JA ENTROU NA CALL AGORA TOCA MÚSICA

    # listinha de amigos disponivel
    if question.lower() == "lista":
        await ctx.send("Lista de audiozinhos: "+' | '.join(lista_audios))
        return
    for audio in lista_audios:
        if audio == question:         
            guild = ctx.guild
            voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
            audio_source = discord.FFmpegPCMAudio(f'./audios/{audio}')
            if not voice_client.is_playing():
                await ctx.send(f"tocando audiozinho {audio}")    
                voice_client.play(audio_source, after=None)
            return
    else:
        await ctx.send("Opa, esse audio n existe.\ndigite '.audio lista' para saber a lista de musicas que vc pode colocar")
    
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

        # FAZ ELE ENTRAR NA CALL
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send('Entre num canal para usar esse comando!')
            
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '100',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
    voice_client.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def acorda(ctx,*,question):
    await ctx.send(ctx.guild.get_member_named(question))
    member = ctx.guild.get_member_named(question)
    
    voice_channel_list = ctx.guild.voice_channels
    voice_channel = ctx.author.voice.channel
    i=0
    while i< 5:
        await member.move_to(random.choice(voice_channel_list))
        # await ctx.member.move_to(random.choice(voice_channel_list))
        time.sleep(0.25)
        i+=1

    #volta pro canal original
    await member.move_to(voice_channel)



@client.command(description="stops and disconnects the bot from voice")
async def leave(ctx):
    
    if ctx.voice_client is None:
        await ctx.send("I'm not in a voice channel, use the join command to make me join")
    else:
        await ctx.voice_client.disconnect()
        await ctx.send('Bot left')

client.run(os.getenv('TOKEN'))

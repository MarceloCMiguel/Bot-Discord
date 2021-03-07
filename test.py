import discord
from discord.ext import commands
import os

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
    'bilbs': 'namora cmg hehe'
}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,activity=discord.Game("o yama no mar"))
    print("We have logged as in {0.user}".format(client))


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

client.run(os.getenv('TOKEN'))

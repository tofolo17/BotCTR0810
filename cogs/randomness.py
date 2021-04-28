import random

from discord.ext import commands

from cogs.long_strings.values import Info

info = Info()


class Randomness(commands.Cog, name="Aleatoriedades"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog foi carregado.')

    @commands.command(brief=info.ping.brief, description=info.ping.description)
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command(aliases=["8ball"], brief=info.eightball.brief, description=info.eightball.description)
    async def eightball(self, ctx, *, question):
        responses = [
            'Sim.',
            'É certo.',
            'Sem dúvida.',
            'Fé que sim.',
            'Com certeza.',
            'Provavelmente.',
            'A meu ver, sim.',
            'Provável que não.',
            'Não conte com isso.',
            'Não, de jeito nenhum.',
            'Tenho minhas dúvidas.',
            'Sim - definitivamente.',
            'Sinais apontam que sim.',
            'Você pode contar com isso.',
            'Meus contatos dizem que não.',
            'Concentre-se e tente de novo.',
            'Olha... Melhor eu ficar quieto.',
            'Pergunte-me depois, não queto te chatear.',
            'Acho melhor você não receber uma resposta para essa pergunta...',
            'Não posso fazer advinhações sobre isso... Pergunta profunda demais para mim.'
        ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(brief=info.clear.brief, description=info.clear.description)
    async def clear(self, ctx, number=None):
        def check_func(msg):
            return not msg.pinned

        if number is not None:
            await ctx.channel.purge(limit=number, check=check_func)
        else:
            await ctx.channel.purge(check=check_func)


def setup(client):
    client.add_cog(Randomness(client))

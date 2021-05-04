import random

from discord.ext import commands


class Randomness(commands.Cog, name="Comandos aleatórios"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog foi carregado.')

    @commands.command(
        brief="Retorna a latência do nosso bot.",
        description='Responde "Pong!" seguido da latência (ou ping) do bot em milissegundos. % ```!ping```'
    )
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command(
        aliases=["8ball"],
        brief="Responde a sua pergunta de forma duvidosa.",
        description="Responde perguntas de advinhação, como o brinquedo Magic 8Ball, inventado nos EUA na década de "
                    "50. % ```!8ball eu vou ser rico?``` ```!eightball o Gilson é o cara?```"
    )
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
        await ctx.send(f'Pergunta: {question}\nResposta: {random.choice(responses)}')

    @commands.command(
        brief="Limpa as mensagens do canal, exceto as fixadas.",
        description="Apaga as mensagens do canal onde foi chamado, exceto as que foram fixadas. O valor padrão é "
                    "cinco. Para apagar to das as mensagens, basta usar `all` como parâmetro. % ```!clear``` "
                    "```!clear 10``` ```!clear all``` "
    )
    async def clear(self, ctx, number="5"):
        def check_func(msg):
            return not msg.pinned

        if number != "all":
            await ctx.channel.purge(limit=int(number), check=check_func)
        else:
            await ctx.channel.purge(check=check_func)


def setup(client):
    client.add_cog(Randomness(client))

import random

from discord.ext import commands


class Randomness(commands.Cog, name="Aleatoriedades"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog foi carregado.')

    @commands.command(brief="Retorna a latência do nosso bot", description="Nadinha.")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command(aliases=["8ball"], brief="Responde de forma duvidosa a sua pergunta.", description="Nadinha.")
    async def eightball(self, ctx, *, question):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes – definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(
        brief="Limpa as mensagens do canal onde é chamado.",
        description="```!clear [quantidade de mensagens]``` % Para limpar uma quantidade específica"
                    " de mensagens:\n```!clear 6```\nPara limpar todo o canal:\n```!clear```"
    )
    async def clear(self, ctx, number=None):
        def check_func(msg):
            return not msg.pinned

        if number is not None:
            await ctx.channel.purge(limit=number, check=check_func)
        else:
            await ctx.channel.purge(check=check_func)


def setup(client):
    client.add_cog(Randomness(client))

import random

from discord.ext import commands

from cogs.useful.classes import Info

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
        responses = info.eightball.responses
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(brief=info.clear.brief, description=info.clear.description)
    async def clear(self, ctx, number="5"):
        def check_func(msg):
            return not msg.pinned

        if number != "all":
            await ctx.channel.purge(limit=int(number), check=check_func)
        else:
            await ctx.channel.purge(check=check_func)


def setup(client):
    client.add_cog(Randomness(client))

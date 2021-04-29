import asyncio

import discord
from discord.ext import commands
from discord.utils import get

from cogs.useful.classes import Info

info = Info()


class Profile(commands.Cog, name="Criação de Card"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog foi carregado.')

    @commands.command(brief="Ainda em desenvolvimento.", description="Ainda em desenvolvimento.")
    async def card(self, ctx):
        def check_func(msg):
            return not msg.pinned

        if ctx.message.channel.name == "👾│card":
            guild = ctx.message.guild
            member = ctx.message.author
            category = ctx.message.channel.category
            new_channel_name = f"👤│{member.name}{member.discriminator}"
            if discord.utils.get(guild.text_channels, name=new_channel_name) is None:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    get(guild.roles, name="Admin"): discord.PermissionOverwrite(read_messages=True),
                    get(guild.roles, name="Robôs"): discord.PermissionOverwrite(read_messages=True),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                new_channel = await guild.create_text_channel(
                    new_channel_name,
                    category=category,
                    overwrites=overwrites
                )
                await ctx.send(f"Dirija-se ao canal `{new_channel.name}` para criar seu card.")
            else:
                await ctx.send(f"Já existe um canal para você. Dirija-se a ele.")
            await asyncio.sleep(30)
            await ctx.channel.purge(check=check_func)
        else:
            await ctx.send("Comando em desenvolvimento. Volte mais tarde.")

    """
    @commands.command()
    async def teste(self, ctx):
        pass
    """


def setup(client):
    client.add_cog(Profile(client))

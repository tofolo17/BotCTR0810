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

    @commands.command(brief="Ainda em desenvolvimento.", description="Ainda em desenvolvimento. % ```!card```")
    async def card(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

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

                # Nickname
                embed = discord.Embed(
                    title="Nickname",
                    description="Envie neste chat seu nome de usuário ou apelido \n\n"
                                "Você tem dois minutos para responder",
                    color=discord.Color.random()
                )
                await new_channel.send(embed=embed)
                try:
                    nickname = await self.client.wait_for("message", check=check, timeout=10)
                    await new_channel.purge()
                    print(nickname)
                except asyncio.TimeoutError:
                    await new_channel.delete()

            else:
                await ctx.send(f"Já existe um canal para você. Dirija-se a ele.")
        else:
            await ctx.send("Comando em desenvolvimento. Volte mais tarde.")


def setup(client):
    client.add_cog(Profile(client))

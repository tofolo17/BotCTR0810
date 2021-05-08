import asyncio

from discord import PermissionOverwrite, Embed, Color
from discord.ext import commands
from discord.utils import get

footer_text = "Você tem cinco minutos para responder cada pergunta. Atente-se para não ter que recomeçar o processo."


class Profile(commands.Cog, name="Criação de Card"):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Ainda em desenvolvimento.", description="Ainda em desenvolvimento. % ```!card```")
    async def card(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == new_channel

        if ctx.channel.name == "👾│card":
            author_info = []
            guild = ctx.guild
            member = ctx.author
            category = ctx.channel.category
            new_channel_name = f"👤│{member.name}{member.discriminator}"
            if get(guild.text_channels, name=new_channel_name) is None:
                overwrites = {
                    guild.default_role: PermissionOverwrite(read_messages=False),
                    get(guild.roles, name="Admin"): PermissionOverwrite(read_messages=True),
                    get(guild.roles, name="🤖  Robôs"): PermissionOverwrite(read_messages=True),
                    member: PermissionOverwrite(read_messages=True)
                }
                new_channel = await guild.create_text_channel(
                    name=new_channel_name,
                    category=category,
                    overwrites=overwrites
                )
                await ctx.send(f"Dirija-se ao canal `{new_channel.name}` para criar seu card.")

                # Nickname
                nickname_embed = Embed(
                    title="📌 Nome de jogador (1/8) 📌",
                    description='Envie ao chat uma mensagem que contenha seu nome de jogador. Pode ser aquele seu '
                                'nickname no lolzinho ou um apelido que você curta. Evite envios do tipo "xxXdestroi'
                                'Noivas99Xxx".\n\nCaso você queira usar seu nickname do Discord, responda com "0".',
                    color=Color.random()
                )
                nickname_embed.set_footer(text=footer_text)
                await new_channel.send(embed=nickname_embed)
                try:
                    nickname = await self.client.wait_for("message", check=check, timeout=300)  # 300 seconds
                    author_info.append(nickname.content if nickname.content != "0" else member.name)
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()

                # Classes
                author_info.append([role.name for role in member.roles if role.name not in ["Admin", "@everyone"]])

                # Avatar
                avatar_embed = Embed(
                    title="📷 Avatar (2/8) 📷",
                    description='Envie ao chat a imagem que será usada no seu perfil de jogador.'
                                '\n\nCaso você queira usar seu avatar do Discord, responda com "0".',
                    color=Color.random()
                )
                avatar_embed.set_footer(text=footer_text)
                await new_channel.send(embed=avatar_embed)
                try:
                    avatar = await self.client.wait_for("message", check=check, timeout=300)
                    author_info.append(avatar.attachments[0].url if avatar.content != "0" else member.avatar_url)
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()
                await new_channel.delete()

            else:
                await ctx.send(f"Já existe um canal para você. Dirija-se a ele.")
        else:
            await ctx.send("Comando em desenvolvimento. Volte mais tarde.")


def setup(client):
    client.add_cog(Profile(client))

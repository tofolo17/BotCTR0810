import asyncio

from discord import PermissionOverwrite, Embed, Color
from discord.ext import commands
from discord.utils import get

footer_text = "Você tem cinco minutos para responder cada pergunta e o card final não é editável. " \
              "Atente-se para não ter que recomeçar o processo."


class Profile(commands.Cog, name="Criação de Card"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        brief="Retorna uma lista que explica detalhadamente os níveis das classes.",
        description="Retorna uma lista que explica detalhadamente os níveis das classes, assim como apresenta a "
                    "sua equivalência através de emojis de livros coloridos. Ou seja, se você reagir com o livro "
                    "de Interesse em uma classe, receberá a classe correspondente a tal reação. % ```!levels```"
    )
    async def levels(self, ctx):
        level_embed = Embed(
            title="Níveis e respectivas descrições",
            description="Para declarar a sua classe, atente-se aos níveis propostos",
            color=Color.random()
        )
        level_embed.add_field(
            name="📘 Interesse",
            value="Entendo pouco ou nada sobre, mas quero aprender",
            inline=False
        )
        level_embed.add_field(
            name="📗 Básico",
            value="Estou dando os meus primeiros passos na área e já possuo certo conhecimento",
            inline=False
        )
        level_embed.add_field(
            name="📙 Intermediário",
            value="Tenho uma base concisa e já posso ampliar meus conhecimentos de forma independente",
            inline=False
        )
        level_embed.add_field(
            name="📕 Avançado",
            value="Domino o básico e algumas vertentes intermediárias / avançadas",
            inline=False
        )
        level_embed.set_footer(
            text="Obs.: seja qual for seu nível, saiba que sempre aprenderemos com o próximo. "
                 "Vamos fazer disso uma troca sincera e proveitosa."
        )
        await ctx.message.channel.send(embed=level_embed)

    @commands.command(
        brief="Cria teu perfil de jogador, baseado nas respostas que você fornecer.",
        description="Ao usá-lo, cria-se um canal privado para que você, caro jogador, "
                    "responda a algumas perguntas. Como retorno, teremos seu perfil "
                    "de jogador, disponível para os outros estudantes. % ```!card```"
    )
    async def card(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == new_channel

        def check2(msg):
            return not msg.pinned

        guild = ctx.guild
        if ctx.channel.name == "👾│cards":
            author_info = []
            extra_fields = {}
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
                    description='Envie a este chat seu nome de jogador. Pode ser aquele seu nickname no lolzinho'
                                ' ou um apelido que você curta. Evite envios do tipo "xxXdestroiNoivas99Xxx".'
                                '\n\nCaso você queira usar seu nickname do Discord, responda com "0".',
                    color=Color.random()
                )
                nickname_embed.set_footer(text=footer_text)
                await new_channel.send(embed=nickname_embed)
                try:
                    nickname = await self.client.wait_for("message", check=check, timeout=300)
                    author_info.append(nickname.content if nickname.content != "0" else member.name)
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()
                    await ctx.channel.purge(check=check2)

                await asyncio.sleep(2)

                # Classes
                author_info.append(
                    [role.mention for role in member.roles if role.name not in ["Admin", "@everyone"]])

                await asyncio.sleep(2)

                # Avatar
                avatar_embed = Embed(
                    title="📷 Avatar (2/8) 📷",
                    description='Envie a este chat a imagem (JPEG ou PNG) que será utilizada no seu perfil de jogador.'
                                '\n\nCaso você queira utilizar seu avatar do Discord, responda com "0".',
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
                    await ctx.channel.purge(check=check2)

                await asyncio.sleep(2)

                # Habilidades de classe
                power_embed = Embed(
                    title="🥇 Poderes de classe (3/8) 🥇",
                    description='Envie a este chat skills relacionadas a sua classe de maior '
                                'domínio. Se você é um(a) Programador(a) de nível Avançado, '
                                'por exemplo, pode responder algo como: "mago(a) em C# 😎".\n\n'
                                'Caso você não queira declarar suas maestrias, responda com "0".',
                    color=Color.random()
                )
                power_embed.set_footer(text=footer_text)
                await new_channel.send(embed=power_embed)
                try:
                    powers = await self.client.wait_for("message", check=check, timeout=300)
                    if powers.content != "0":
                        extra_fields["Habilidades de classe"] = powers.content
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()
                    await ctx.channel.purge(check=check2)

                await asyncio.sleep(2)

                # Habilidades especiais
                specific_power_embed = Embed(
                    title="🏆 Poderes especiais (4/8) 🏆",
                    description='Envie a este chat sua skill especial! Estas são habilidades que não são '
                                'diretamente relacionadas a esta disciplina, mas sim, a sua trajetória! '
                                'Se você é das Ciências Biológicas, por exemplo, pode responder algo como: '
                                '"Sei o nome científico de todos os gorilas que ainda não foram extintos ✌🏻".\n\n'
                                'Caso você não queira declarar suas maestrias, responda com "0".',
                    color=Color.random()
                )
                specific_power_embed.set_footer(text=footer_text)
                await new_channel.send(embed=specific_power_embed)
                try:
                    specific_power = await self.client.wait_for("message", check=check, timeout=300)
                    if specific_power.content != "0":
                        extra_fields["Habilidades especiais"] = specific_power.content
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()
                    await ctx.channel.purge(check=check2)

                await asyncio.sleep(2)

                # Interesses de aprendizado
                interests_embed = Embed(
                    title="📚 Interesses de aprendizado (5/8) 📚",
                    description='Envie a este chat seus interesses de aprendizado, tanto '
                                'disciplinares, quanto gerais. Se você está interessado(a) '
                                'em Programação, por exemplo, pode responder algo como: '
                                '"Quanto aos games, me interesso pela criação de mapas '
                                'procedurais. Fora isso, também me amarro em IA.".\n\n'
                                'Caso você não queira declará-los, responda com "0".',
                    color=Color.random()
                )
                interests_embed.set_footer(text=footer_text)
                await new_channel.send(embed=interests_embed)
                try:
                    interest = await self.client.wait_for("message", check=check, timeout=300)
                    if interest.content != "0":
                        extra_fields["Interesses de aprendizado"] = interest.content
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()
                    await ctx.channel.purge(check=check2)

                await asyncio.sleep(2)

                # Interesses temáticos
                themes_embed = Embed(
                    title="🎲 Interesses temáticos (6/8) 🎲",
                    description='Envie a este chat seus interesses temáticos relacionados a criação de um jogo. '
                                'Exemplo: "quero fazer um jogo não digital de RPG com a temática Cyberpunk".'
                                '\n\nCaso você não queira declará-los, responda com "0".',
                    color=Color.random()
                )
                themes_embed.set_footer(text=footer_text)
                await new_channel.send(embed=themes_embed)
                try:
                    theme = await self.client.wait_for("message", check=check, timeout=300)
                    if theme.content != "0":
                        extra_fields["Interesses temáticos"] = theme.content
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()
                    await ctx.channel.purge(check=check2)

                await asyncio.sleep(2)

                # Referências artísticas
                reference_embed = Embed(
                    title="🎭 Referências artísticas (7/8) 🎭",
                    description='Envie a este chat quaisquer referências artísticas de seu gosto. '
                                'O desenvolvedor desse bot provavelmente teria Paramore incluído '
                                'na resposta.\n\nCaso você não queira apresentá-los, responda com "0".',
                    color=Color.random()
                )
                reference_embed.set_footer(text=footer_text)
                await new_channel.send(embed=reference_embed)
                try:
                    reference = await self.client.wait_for("message", check=check, timeout=300)
                    if reference.content != "0":
                        extra_fields["Referências artísticas"] = reference.content
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()
                    await ctx.channel.purge(check=check2)

                await asyncio.sleep(2)

                # Redes sociais
                social_embed = Embed(
                    title="🔎 Social (8/8) 🔎",
                    description='Por fim, envie a este chat seu instagram/portfolio/github/link/site ou o que lhe for '
                                'conveniente (não utilize @).\n\nCaso você não queira se tornar famoso(a) diante '
                                'de nós, responda com "0".',
                    color=Color.random()
                )
                social_embed.set_footer(text=footer_text)
                await new_channel.send(embed=social_embed)
                try:
                    social = await self.client.wait_for("message", check=check, timeout=300)
                    if social.content != "0":
                        extra_fields["Redes sociais"] = social.content
                    await new_channel.purge()
                except asyncio.TimeoutError:
                    await new_channel.delete()
                    await ctx.channel.purge(check=check2)
                await new_channel.delete()

                await asyncio.sleep(2)

                # Card do jogador
                player_embed = Embed(
                    title=author_info[0],
                    description=" ".join(author_info[1]),
                    color=Color.random()
                )
                player_embed.set_thumbnail(url=author_info[2])
                for k, v in extra_fields.items():
                    player_embed.add_field(name=f'{k}', value=f'{v}', inline=False)
                player_embed_message = await ctx.send(embed=player_embed)
                await player_embed_message.pin()
                await ctx.channel.purge(check=check2)

            else:
                await ctx.send(f"Já existe um canal para você. Dirija-se a ele.")
        else:
            card_channel_name = "👾│cards"
            await ctx.send(
                f"Este comando só funciona no canal {get(guild.text_channels, name=card_channel_name).mention}."
            )


def setup(client):
    client.add_cog(Profile(client))

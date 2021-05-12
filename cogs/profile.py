import asyncio

from discord import PermissionOverwrite
from discord.ext import commands
from discord.utils import get

from embeds import *

card_channel_name = "👾│cards"
footer_text = "Você tem cinco minutos para responder esta mensagem. Atente-se para não ter que recomeçar o processo."


async def create_secret_channel(guild, category, member, channel_name):
    overwrites = {
        guild.default_role: PermissionOverwrite(read_messages=False),
        get(guild.roles, name="Admin"): PermissionOverwrite(read_messages=True),
        get(guild.roles, name="🤖  Robôs"): PermissionOverwrite(read_messages=True),
        member: PermissionOverwrite(read_messages=True)
    }
    new_channel = await guild.create_text_channel(
        name=channel_name,
        category=category,
        overwrites=overwrites
    )
    return new_channel


async def has_card(channel, member, get_message=False):
    messages = await channel.history(limit=None).flatten()
    for message in messages:
        for mention in message.mentions:
            if mention.discriminator == member.discriminator:
                if get_message:
                    return message
                else:
                    return True


async def send_embed(embed_class, channel):
    avatar_embed = embed_class
    avatar_embed.set_footer(text=footer_text)
    await channel.send(embed=avatar_embed)


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
        await ctx.channel.send(embed=level_embed)

    @commands.command(
        brief="Cria teu perfil de jogador, baseado nas respostas que você fornecer.",
        description="Ao usá-lo, cria-se um canal privado para que você, caro jogador, "
                    "responda a algumas perguntas. Como retorno, teremos seu perfil "
                    "de jogador, disponível para os outros estudantes. % ```!card```"
    )
    async def card(self, ctx):
        def channel_check(msg):
            return msg.author == ctx.author and msg.channel == secret_channel

        guild = ctx.guild
        channel = ctx.channel
        if channel.name == card_channel_name:
            extra_info = {}
            member_info = []
            member = ctx.author
            category = channel.category
            secret_channel_name = f"👤│{member.name}{member.discriminator}"
            if get(guild.text_channels, name=secret_channel_name) is None and not await has_card(channel, member):
                secret_channel = await create_secret_channel(guild, category, member, secret_channel_name)
                await ctx.send(f"Dirija-se ao canal `{secret_channel.name}` para criar seu card.", delete_after=15)

                # Primeira mensagem
                hello_embed = Embed(
                    title="😎 Vamos começar! 😎",
                    description="Para criar seu perfil de jogador, responda as próximas "
                                "oito perguntas (todas simples e não intrusivas)."
                )
                await secret_channel.send(embed=hello_embed)

                # Nickname
                await send_embed(NicknameEmbed(), secret_channel)
                try:
                    nickname = await self.client.wait_for("message", check=channel_check, timeout=300)
                    member_info.append(nickname.content if nickname.content != "0" else member.name)
                except asyncio.TimeoutError:
                    await secret_channel.delete()

                # Classes
                member_info.append([role.mention for role in member.roles if role.name != "@everyone"])

                # Avatar
                avatar_embed = AvatarEmbed()
                avatar_embed.set_footer(text=footer_text)
                await secret_channel.send(embed=avatar_embed)
                try:
                    avatar = await self.client.wait_for("message", check=channel_check, timeout=300)
                    member_info.append(avatar.attachments[0].url if avatar.content != "0" else member.avatar_url)
                except asyncio.TimeoutError:
                    await secret_channel.delete()

                for embed_class in [
                    PowerEmbed(), SpecificPowerEmbed(), InterestsEmbed(),
                    ThemesEmbed(), ReferencesEmbed(), SocialEmbed()
                ]:
                    await send_embed(embed_class, secret_channel)
                    try:
                        data = await self.client.wait_for("message", check=channel_check, timeout=300)
                        if data.content != "0":
                            extra_info[embed_class.title] = data.content
                    except asyncio.TimeoutError:
                        await secret_channel.delete()
                await secret_channel.delete()

                # Card do jogador
                player_embed = Embed(
                    title=member_info[0],
                    description=" ".join(member_info[1]),
                    color=Color.random()
                )
                player_embed.set_thumbnail(url=member_info[2])
                for k, v in extra_info.items():
                    player_embed.add_field(name=f'{k}', value=f'{v}', inline=False)
                player_embed_message = await ctx.send(member.mention, embed=player_embed)
                await player_embed_message.pin()

            else:
                await ctx.send(
                    f"Das duas, uma: ou seu canal já foi criado, ou você já tem um card. Caso a "
                    f"segunda, apague teu card atual para criar um novo. Considere editá-lo antes disso.",
                    delete_after=15
                )
        else:
            await ctx.send(
                f"Este comando só funciona no canal {get(guild.text_channels, name=card_channel_name).mention}.",
                delete_after=15
            )

    @commands.command(
        brief="Edita teu perfil de jogador.",
        description="Ao usá-lo, cria-se um canal privado para que você, caro jogador, atualize seu "
                    "perfil de jogador com base nas suas novas respostas. % ```!edit```"
    )
    async def edit(self, ctx):
        def reaction_check(r, m):
            return not m.bot

        def channel_check(msg):
            return msg.author == ctx.author and msg.channel == secret_channel

        guild = ctx.guild
        cards_channel = ctx.channel
        if cards_channel.name == card_channel_name:
            member = ctx.author
            category = cards_channel.category
            new_channel_name = f"👤│{member.name}{member.discriminator}"
            message = await has_card(cards_channel, member, get_message=True)
            if get(guild.text_channels, name=new_channel_name) is None and message is not None:
                secret_channel = await create_secret_channel(guild, category, member, new_channel_name)
                await ctx.send(f"Dirija-se ao canal `{secret_channel.name}` para editar seu card.", delete_after=15)

                # Interação usuário
                edit_embed = Embed(
                    title="😎 Bora alterar esse perfil de jogador? 😎",
                    description="Reaja a esta mensagem para editar ou acrescentar uma "
                                "informação de acordo com a seguinte tabela:",
                    color=Color.random()
                )
                edit_embed.add_field(name="📌 Nome de jogador 📌", value="1️⃣", inline=False)
                edit_embed.add_field(name="📷 Avatar 📷", value="2️⃣", inline=False)
                edit_embed.add_field(name="🥇 Habilidades de classe 🥇", value="3️⃣", inline=False)
                edit_embed.add_field(name="🏆 Habilidades especiais 🏆", value="4️⃣", inline=False)
                edit_embed.add_field(name="📚 Interesses de aprendizado 📚", value="5️⃣", inline=False)
                edit_embed.add_field(name="🎲 Interesses temáticos 🎲", value="6️⃣", inline=False)
                edit_embed.add_field(name="🎭 Referências artísticas 🎭", value="7️⃣", inline=False)
                edit_embed.add_field(name="🔎 Social 🔎", value="8️⃣", inline=False)
                edit_embed.add_field(name="🔖 Atualizar classes 🔖", value="9️⃣", inline=False)
                edit_embed.add_field(name="❌ Sair ❌", value="0️⃣", inline=False)
                edit_embed.set_footer(text=footer_text)

                while True:
                    embed_dict = message.embeds[0].to_dict()
                    edit_message = await secret_channel.send(embed=edit_embed)
                    for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "0️⃣"]:
                        await edit_message.add_reaction(emoji)

                    try:
                        reaction, user = await self.client.wait_for("reaction_add", check=reaction_check, timeout=300)
                    except asyncio.TimeoutError:
                        await secret_channel.delete()
                    else:

                        # Nickname
                        if reaction.emoji == "1️⃣":
                            await send_embed(NicknameEmbed(), secret_channel)
                            try:
                                nickname = await self.client.wait_for("message", check=channel_check, timeout=300)
                            except asyncio.TimeoutError:
                                await secret_channel.delete()
                            else:
                                embed_dict["title"] = nickname.content if nickname.content != "0" else member.name
                                new_embed = Embed.from_dict(embed_dict)
                                await message.edit(embed=new_embed)

                        # Avatar
                        elif reaction.emoji == "2️⃣":
                            discord_avatar = bool()
                            await send_embed(AvatarEmbed(), secret_channel)
                            try:
                                avatar = await self.client.wait_for("message", check=channel_check, timeout=300)
                            except asyncio.TimeoutError:
                                await secret_channel.delete()
                            else:
                                if avatar.content != "0":
                                    embed_dict['thumbnail']['url'] = avatar.attachments[0].url
                                else:
                                    discord_avatar = True
                                new_embed = Embed.from_dict(embed_dict)
                                if discord_avatar:
                                    new_embed.set_thumbnail(url=member.avatar_url)
                                await message.edit(embed=new_embed)

                        # Atualizar classes
                        elif reaction.emoji == "9️⃣":
                            roles = [role.mention for role in member.roles if role.name != "@everyone"]
                            embed_dict['description'] = " ".join(roles)
                            new_embed = Embed.from_dict(embed_dict)
                            await message.edit(embed=new_embed)

                        # Sair
                        elif reaction.emoji == "0️⃣":
                            await secret_channel.delete()

                        # Fields
                        for field_emoji in [
                            ["3️⃣", PowerEmbed()],
                            ["4️⃣", SpecificPowerEmbed()],
                            ["5️⃣", InterestsEmbed()],
                            ["6️⃣", ThemesEmbed()],
                            ["7️⃣", ReferencesEmbed()],
                            ["8️⃣", SocialEmbed()]
                        ]:
                            if reaction.emoji == field_emoji[0]:
                                reacted_class = field_emoji[1]
                                await send_embed(reacted_class, secret_channel)
                                try:
                                    data = await self.client.wait_for("message", check=channel_check, timeout=300)
                                except asyncio.TimeoutError:
                                    await secret_channel.delete()
                                else:
                                    not_exists = True
                                    for field in embed_dict["fields"]:
                                        if field['name'] == reacted_class.title:
                                            field['value'] = data.content
                                            not_exists = False
                                    if not_exists:
                                        print("a")
                                        embed_dict["fields"].append(
                                            {'name': reacted_class.title, 'value': data.content}
                                        )
                                new_embed = Embed.from_dict(embed_dict)
                                await message.edit(embed=new_embed)

                        await secret_channel.send("Tudo feito.")

            else:
                await ctx.send(
                    f"Das duas, uma: ou seu canal já foi criado, ou você não possui um card para editar.",
                    delete_after=15
                )
        else:
            await ctx.send(
                f"Este comando só funciona no canal {get(guild.text_channels, name=card_channel_name).mention}.",
                delete_after=15
            )


def setup(client):
    client.add_cog(Profile(client))

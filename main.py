import asyncio
import os

from discord import Embed, Colour
from discord.ext import commands

from cogs.useful.classes import *

intents = discord.Intents.default()
intents.guild_messages = True

client = commands.Bot(command_prefix="!", intents=intents)
info = Info()


@client.event
async def on_ready():
    while True:
        activity = info.status.get_status()
        await client.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(30)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Comando inexistente!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Lhe falta permissões!')


@client.event
async def on_raw_reaction_add(payload=None):
    member = payload.member
    channel = client.get_channel(payload.channel_id)
    if channel.name == "🆔│cargos" and not member.bot:
        emoji = payload.emoji.name
        emoji_list = ["📕", "📙", "📗", "📘"]
        guild = client.get_guild(payload.guild_id)
        message = await channel.fetch_message(payload.message_id)
        role_list = [role for role in guild.roles if role.colour == message.embeds[0].colour]
        for role in member.roles:
            if role in role_list[:-1]:
                await member.remove_roles(role)
                await message.remove_reaction(emoji_list[role_list.index(role)], member)
        emoji_index = emoji_list.index(emoji)
        await member.add_roles(role_list[-1])
        await member.add_roles(role_list[emoji_index])


@client.event
async def on_raw_reaction_remove(payload=None):
    channel = client.get_channel(payload.channel_id)
    if channel.name == "🆔│cargos":
        guild = client.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        reactions = [reaction.count for reaction in message.reactions]
        if sum(reactions) >= 4:
            for role in guild.roles:
                if role.colour == message.embeds[0].colour:
                    await member.remove_roles(role)


@client.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, red, green, blue, name, create="False"):
    guild = ctx.guild
    perms = guild.default_role.permissions
    color = Colour.from_rgb(int(red), int(green), int(blue))
    for i in [name, "Interesse", "Básico", "Intermediário", "Avançado"]:
        if create == "True":
            await guild.create_role(name=i, colour=color, permissions=perms)
        else:
            pass
    message = await ctx.send(embed=Embed(title=name, color=color))
    emoji_list = ["📘", "📗", "📙", "📕"]
    for emoji in emoji_list:
        await message.add_reaction(emoji)


@client.command()
@commands.has_permissions(manage_roles=True)
async def dr(ctx, r, g, b):
    for role in ctx.message.guild.roles:
        if role.color == Colour.from_rgb(int(r), int(g), int(b)):
            await role.delete()


@client.command()
@commands.has_permissions(manage_roles=True)
async def embed(ctx):
    level_embed = discord.Embed(
        title="Níveis e respectivas descrições",
        description="Para declarar a sua classe, atente-se aos níveis propostos",
        color=discord.Color.random()
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


class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        help_embed = Embed(title="Lista de comandos e categorias", color=discord.Color.random())
        mapping.popitem()
        for cog, coms in mapping.items():
            command_signatures = [f'{c.brief}```\n{self.get_command_signature(c)}```' for c in coms]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name")
                help_embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        help_embed.set_footer(text=ending_note)
        channel = self.get_destination()
        await channel.send(embed=help_embed)

    async def send_command_help(self, command):
        command_help_embed = Embed(title=self.get_command_signature(command), color=discord.Color.random())
        command_help_embed.add_field(name="Descrição", value=command.description.split("%")[0], inline=False)
        command_help_embed.add_field(name="Exemplos", value=command.description.split("%")[1])
        channel = self.get_destination()
        await channel.send(embed=command_help_embed)


client.help_command = MyHelp()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.environ.get('BOT_TOKEN'))

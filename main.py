import asyncio
import os
from random import choice, randint

from discord import Game, Activity, ActivityType, Status, Intents
from discord.ext import commands
from discord.utils import get

from embeds import *

intents = Intents.default()
intents.guild_messages = True
intents.reactions = True

client = commands.Bot(command_prefix="!", intents=intents)


class BotStatus:
    def __init__(self):
        self.data = {
            "playing": [
                "Sky: Children of the Light",
                "GRIS",
                "Hyper Light Drifter",
                "Katana ZERO",
                "Celeste",
                "The First Tree",
                "Hollow Knight",
                "The Legend of Zelda",
                "Genshin Impact",
                "COD Zombies",
                "Minecraft",
                "Garticphone",
                "Metal Gear",
                "Hotline Miami",
                "Stardew Valley"
            ],
            "listening": [
                "A trilha sonora de Undertale",
                "ALL OUT das K/DA",
                "o Joel cantar pra Ellie",
                "A trilha sonora de Life is Strange e chorando muito",
                "A trilha sonora de Cry of Fear",
                "A trilha sonora de Bloodborne"
            ]
        }

    def get_status(self):
        active_status = choice(list(self.data.keys()))
        status_value = self.data[active_status][randint(0, len(self.data[active_status]) - 1)]
        if active_status == "playing":
            return Game(name=f'🎮 {status_value} || !help')
        elif active_status == "listening":
            return Activity(type=ActivityType.listening, name=f'🎶 {status_value} || !help')


@client.event
async def on_ready():
    while True:
        activity = BotStatus().get_status()
        await client.change_presence(status=Status.online, activity=activity)
        await asyncio.sleep(3000)


@client.event
async def on_message(message):
    if message.content in ["!card", "!edit"]:
        await message.delete(delay=15)
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Comando inexistente!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Lhe falta permissões!')


@client.event
async def on_raw_reaction_add(payload=None):
    member = payload.member
    guild = client.get_guild(payload.guild_id)
    channel = client.get_channel(payload.channel_id)
    if channel.name == "🆔│classes" and not member.bot:
        message = await channel.fetch_message(payload.message_id)
        member_roles = [role for role in member.roles]
        guild_roles = [
            role for role in guild.roles if role.colour == message.embeds[0].colour
        ]
        if len(member_roles) == 1:
            await member.add_roles(get(guild.roles, id=839136218436075558))
        if payload is not None:
            await member.add_roles(guild_roles[-1])
            if payload.emoji.name == "📕":
                await member.add_roles(guild_roles[0])
            elif payload.emoji.name == "📙":
                await member.add_roles(guild_roles[1])
            elif payload.emoji.name == "📗":
                await member.add_roles(guild_roles[2])
            else:
                await member.add_roles(guild_roles[3])


@client.event
async def on_raw_reaction_remove(payload=None):
    guild = client.get_guild(payload.guild_id)
    channel = client.get_channel(payload.channel_id)
    member = await guild.fetch_member(payload.user_id)
    if channel.name == "🆔│classes":
        message = await channel.fetch_message(payload.message_id)
        guild_roles = [role for role in guild.roles if role.colour == message.embeds[0].colour]
        colored_member_roles = [role for role in member.roles if role.colour == message.embeds[0].colour]
        if payload is not None:
            if len(colored_member_roles) == 2:
                await member.remove_roles(guild_roles[-1])
            if payload.emoji.name == "📕":
                await member.remove_roles(guild_roles[0])
            elif payload.emoji.name == "📙":
                await member.remove_roles(guild_roles[1])
            elif payload.emoji.name == "📗":
                await member.remove_roles(guild_roles[2])
            else:
                await member.remove_roles(guild_roles[3])
        member = await guild.fetch_member(payload.user_id)
        if len(member.roles) == 2:
            await member.remove_roles(get(guild.roles, id=839136218436075558))


# -- Estudos e testes --
"""
@client.command()
@commands.has_permissions(manage_roles=True)
async def mentions(ctx):
    messages = await ctx.channel.history(limit=None).flatten()
    for message in messages:
        for m in message.mentions:
            if m.discriminator == ctx.author.discriminator:
                await ctx.send("Canal.")


@client.command()
@commands.has_permissions(manage_roles=True)
async def mention(ctx):
    await ctx.send(ctx.author.mention)


@client.command()
@commands.has_permissions(manage_roles=True)
async def join(ctx):
    guild = ctx.guild
    vc = guild.voice_channels[0]
    await vc.connect()


@client.command()
@commands.has_permissions(manage_roles=True)
async def leave(ctx):
    vc = ctx.voice_client
    await vc.disconnect()


@client.command()
@commands.has_permissions(manage_roles=True)
async def play(ctx, url):
    vc = ctx.voice_client
    player = await vc.create_ytdl_player(url)
    player.start()


@client.command()
@commands.has_permissions(manage_roles=True)
async def resend(ctx):
    files = []
    for file in ctx.message.attachments:
        fp = BytesIO()
        await file.save(fp)
        files.append(File(fp, filename=file.filename, spoiler=file.is_spoiler()))
    await ctx.send(files=files)


@client.command()
@commands.has_permissions(manage_roles=True)
async def add(ctx, msg_id, member: Member):
    message = await ctx.channel.fetch_message(msg_id)
    await message.edit(content=member.mention, embed=message.embeds[0])


@client.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, red, green, blue, name, create="False"):
    guild = ctx.guild
    color = Colour.from_rgb(int(red), int(green), int(blue))
    for role_name in [name, "Interesse", "Básico", "Intermediário", "Avançado"]:
        if create == "True":
            await guild.create_role(name=role_name, colour=color, permissions=guild.default_role.permissions)
        else:
            pass
    message = await ctx.send(embed=Embed(title=name, color=color))
    for emoji in ["📘", "📗", "📙", "📕"]:
        await message.add_reaction(emoji)


@client.command()
@commands.has_permissions(manage_roles=True)
async def dr(ctx, r, g, b):
    for role in ctx.guild.roles:
        if role.color == Colour.from_rgb(int(r), int(g), int(b)):
            await role.delete()


@client.command()
async def up(ctx, msg_id):
    title_list = []
    channel = ctx.channel
    for embed_class in [
        PowerEmbed(), SpecificPowerEmbed(), InterestsEmbed(),
        ThemesEmbed(), ReferencesEmbed(), SocialEmbed()
    ]:
        title_list.append(embed_class.title)
    message = await channel.fetch_message(msg_id)
    embed_dict = message.embeds[0].to_dict()
    for i in range(len(title_list)):
        for j in range(len(embed_dict['fields'])):
            if embed_dict['fields'][j]['name'] in title_list[i]:
                embed_dict['fields'][j]['name'] = title_list[i]
    new_embed = Embed.from_dict(embed_dict)
    await message.edit(embed=new_embed)
"""


# ----------------------


class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        help_embed = Embed(title="Lista de comandos e categorias", color=Color.random())
        mapping.popitem()
        for cog, coms in mapping.items():
            command_signatures = [f'{c.brief}```\n{self.get_command_signature(c)}```' for c in coms]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name")
                help_embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        help_embed.set_footer(text="Para mais informações, escreva !help <comando>.")
        channel = self.get_destination()
        await channel.send(embed=help_embed)

    async def send_command_help(self, command):
        command_help_embed = Embed(title=self.get_command_signature(command), color=Color.random())
        command_help_embed.add_field(name="Descrição", value=command.description.split("%")[0], inline=False)
        command_help_embed.add_field(name="Exemplos", value=command.description.split("%")[1])
        channel = self.get_destination()
        await channel.send(embed=command_help_embed)


client.help_command = MyHelp()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run()

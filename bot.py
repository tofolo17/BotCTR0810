import os

import discord
from discord import Embed
from discord.ext import commands

from cogs.long_strings.values import ending_note

client = commands.Bot(command_prefix="!")


class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = Embed(title="Lista de comandos e categorias", color=discord.Color.random())
        mapping.popitem()
        for cog, coms in mapping.items():
            command_signatures = [f'{c.brief}```\n{self.get_command_signature(c)}```' for c in coms]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        embed.add_field(name=chr(173), value=ending_note)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = Embed(title=self.get_command_signature(command), color=discord.Color.random())
        embed.add_field(name="Descrição", value=command.description.split("%")[0], inline=False)
        embed.add_field(name="Exemplos", value=command.description.split("%")[1])
        channel = self.get_destination()
        await channel.send(embed=embed)


client.help_command = MyHelp()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.environ.get('BOT_TOKEN'))

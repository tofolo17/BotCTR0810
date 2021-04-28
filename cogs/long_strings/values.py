import random

import discord

ending_note = "Para mais informações, escreva `!help <comando>`.\n" \
              "Obs.: como ainda não hospedamos o bot, ele não funciona" \
              " a todo instante. Verifique se o mesmo está online."


class Ping:
    def __init__(self):
        self.brief = "Retorna a latência do nosso bot."
        self.description = 'Responde "Pong!" seguido da latência (ou ping) do bot em milissegundos. %' \
                           '```!ping```'


class Eightball:
    def __init__(self):
        self.brief = "Responde a sua pergunta de forma duvidosa."
        self.description = "Responde perguntas de advinhação, como o brinquedo Magic 8Ball, inventado nos EUA na" \
                           " década de 50. % ```!8ball eu vou ser rico?``` ```!eightball o Gilson é o cara?```"


class Clear:
    def __init__(self):
        self.brief = "Limpa as mensagens do canal, exceto as fixadas."
        self.description = "Apaga as mensagens do canal onde foi chamado, exeto as que foram fixadas. Para apagar to" \
                           "das as mensagens, basta não acrescentar nenhum parâmetro. % ```!clear 10``` ```!clear```"


class Status:
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
                "COD Zombies"
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
        active_status = random.choice(list(self.data.keys()))
        status_value = self.data[active_status][random.randint(0, len(self.data[active_status]) - 1)]
        if active_status == "playing":
            return discord.Game(name=f'🎮 {status_value}')
        elif active_status == "listening":
            return discord.Activity(type=discord.ActivityType.listening, name=f'🎶 {status_value}')


class Info:
    def __init__(self):
        self.ping = Ping()
        self.clear = Clear()
        self.status = Status()
        self.eightball = Eightball()

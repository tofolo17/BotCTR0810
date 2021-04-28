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


class Info:
    def __init__(self):
        self.ping = Ping()
        self.clear = Clear()
        self.eightball = Eightball()

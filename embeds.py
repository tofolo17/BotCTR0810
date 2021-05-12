from discord import Embed, Color


class NicknameEmbed(Embed):
    def __init__(self):
        super().__init__(
            title="📌 Nome de jogador 📌",
            description='Envie a este chat seu nome de jogador. Pode ser aquele seu nickname no lolzinho'
                        ' ou um apelido que você curta. Evite envios do tipo "xxXdestroiNoivas99Xxx".'
                        '\n\nCaso você queira usar seu nickname do Discord, responda com "0".',
            color=Color.random()
        )


class AvatarEmbed(Embed):
    def __init__(self):
        super().__init__(
            title="📷 Avatar 📷",
            description='Envie a este chat a imagem (JPEG ou PNG) que será utilizada no seu perfil de jogador.'
                        '\n\nCaso você queira utilizar seu avatar do Discord, responda com "0".',
            color=Color.random()
        )


class PowerEmbed(Embed):
    def __init__(self):
        super().__init__(
            title="🥇 Habilidades de classe 🥇",
            description='Envie a este chat skills relacionadas a sua classe de maior '
                        'domínio. Se você é um(a) Programador(a) de nível Avançado, '
                        'por exemplo, pode responder algo como: "mago(a) em C# 😎".\n\n'
                        'Caso você não queira declarar suas maestrias, responda com "0".',
            color=Color.random()
        )


class SpecificPowerEmbed(Embed):
    def __init__(self):
        super().__init__(
            title="🏆 Habilidades especiais 🏆",
            description='Envie a este chat sua skill especial! Estas são habilidades que não são '
                        'diretamente relacionadas a esta disciplina, mas sim, a sua trajetória! '
                        'Se você é das Ciências Biológicas, por exemplo, pode responder algo como: '
                        '"Sei o nome científico de todos os gorilas que ainda não foram extintos ✌🏻".\n\n'
                        'Caso você não queira declarar suas maestrias, responda com "0".',
            color=Color.random()
        )


class InterestsEmbed(Embed):
    def __init__(self):
        super().__init__(
            title="📚 Interesses de aprendizado 📚",
            description='Envie a este chat seus interesses de aprendizado, tanto '
                        'disciplinares, quanto gerais. Se você está interessado(a) '
                        'em Programação, por exemplo, pode responder algo como: '
                        '"Quanto aos games, me interesso pela criação de mapas '
                        'procedurais. Fora isso, também me amarro em IA.".\n\n'
                        'Caso você não queira declará-los, responda com "0".',
            color=Color.random()
        )


class ThemesEmbed(Embed):
    def __init__(self):
        super().__init__(
            title="🎲 Interesses temáticos 🎲",
            description='Envie a este chat seus interesses temáticos relacionados a criação de um jogo. '
                        'Exemplo: "quero fazer um jogo não digital de RPG com a temática Cyberpunk".'
                        '\n\nCaso você não queira declará-los, responda com "0".',
            color=Color.random()
        )


class ReferencesEmbed(Embed):
    def __init__(self):
        super().__init__(
            title="🎭 Referências artísticas 🎭",
            description='Envie a este chat quaisquer referências artísticas de seu gosto. '
                        'O desenvolvedor desse bot provavelmente teria Paramore incluído '
                        'na resposta.\n\nCaso você não queira apresentá-los, responda com "0".',
            color=Color.random()
        )


class SocialEmbed(Embed):
    def __init__(self):
        super().__init__(
            title="🔎 Social 🔎",
            description='Por fim, envie a este chat seu instagram/portfolio/github/link/site ou o que lhe for '
                        'conveniente (não utilize @).\n\nCaso você não queira se tornar famoso(a) diante '
                        'de nós, responda com "0".',
            color=Color.random()
        )

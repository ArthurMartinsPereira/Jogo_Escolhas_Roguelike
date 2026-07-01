from Events.base import Event
from Events.registry import register_event

@register_event("dwarven_smith")
class DwarvenSmith(Event):

    title = "Anão Ferreiro"

    description = (
        "Você encontra um velho Anão Ferreiro na estrada,"
        "Ele está vendendo alguns equipamentos."
    )

    def run(self, player):

        print(self.description)

        print("1 - Loja")
        print("2 - Ignorar")



@register_event("black_smith")
class Smith(Event):
    title = "Ferreiro"

    description = (
        "Você entra em uma Ferraria"
        "Muitas armas e armaduras estão à venda."
    )

    def run(self, player):
        print(self.description)

        print("1 - Loja")
        print("2 - Ignorar")

@register_event("magic_shop")
class MagicShop(Event):
    title = "Loja Mágica"

    description = (
        "Você entra em uma loja de items mágicos"
        "Muitas varinhas, amuletos, cajados e poções estão à venda."
    )

    def run(self, player):
        print(self.description)

        print("1 - Loja")
        print("2 - Ignorar")

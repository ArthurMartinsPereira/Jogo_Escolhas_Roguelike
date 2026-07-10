from Events.base import Event
from Events.registry import register_event

@register_event("dwarven_smith")
class DwarvenSmith(Event):

    title = "Anão Ferreiro"
    category = "store"

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
    category = "store"

    description = (
        "Você entra em uma Ferraria"
        "Muitas armas e armaduras estão à venda."
    )

    def run(self, player):
        print(self.description)

        print("1 - Loja")
        print("2 - Ignorar")


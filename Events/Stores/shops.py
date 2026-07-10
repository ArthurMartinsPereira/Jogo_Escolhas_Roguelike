from Events.base import Event
from Events.registry import register_event

@register_event("magic_shop")
class MagicShop(Event):

    title = "Loja Mágica"
    category = "store"

    description = (
        "Você entra em uma loja de items mágicos"
        "Muitas varinhas, amuletos, cajados e poções estão à venda."
    )

    def run(self, player):
        print(self.description)

        print("1 - Loja")
        print("2 - Ignorar")

@register_event("adventurer_shop")
class MagicShop(Event):

    title = "Loja dos Aventureiros"
    category = "store"

    description = (
        "Você entra em uma loja de items para aventureiros"
        "Muitas armas, armaduras e ferramentas estão à venda."
    )

    def run(self, player):
        print(self.description)

        print("1 - Loja")
        print("2 - Ignorar")
from Events.base import Event
from Events.registry import register_event
from Events.Stores_Interface import StoreInterface
from Events.Stores_Base import Store


@register_event("dwarven_smith")
class DwarvenSmith(Event):

    title = "Anão Ferreiro"
    category = "store"
    unique = True

    description = (
        "Você encontra um velho Anão Ferreiro na estrada. "
        "Ele está vendendo alguns equipamentos."
    )

    def run(self, player):

        self.show()

        choice = self.choose(
            "Ver a loja",
            "Ignorar"
        )

        if choice == 1:

            store = Store([
                "steel_longsword",
                "iron_sword",
                "iron_armor",
                "vampire_ring"
            ])

            store.generate_stock(player)

            interface = StoreInterface(store)
            interface.show(player)



@register_event("black_smith")
class Smith(Event):

    title = "Ferreiro"
    category = "store"
    unique = False

    description = (
        "Você entra em uma Ferraria"
        "Muitas armas e armaduras estão à venda."
    )

    def run(self, player):

        self.show()

        choice = self.choose(
            "Ver a loja",
            "Ignorar"
        )

        if choice == 1:

            store = Store([
                "iron_sword",
                "iron_armor",
                "steel_longsword"
            ])

            store.generate_stock(player)

            interface = StoreInterface(store)
            interface.show(player)

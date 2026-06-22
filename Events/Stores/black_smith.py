from Events.base import Event
from Events.registry import register_event


@register_event("dwarven_smith")
class DwarvenSmith(Event):

    title = "Anão Ferreiro"

    description = (
        "Você encontra um Anão Ferreiro "
        "ele está vendendo alguns items."
    )

    def run(self, player):

        print(self.description)

        print("1 - Loja")
        print("2 - Ignorar")
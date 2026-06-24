from Events.base import Event
from Events.registry import register_event

@register_event("goblin")
class Goblin(Event):

    title = "Goblin"

    description = (
        "Um globin bloqueia seu caminho,"
        "Você saca sua arma e se prepara."
    )

    def run(self, player):
        print(self.description)
        print("1 - Atacar primeiro")
        print("2 - Esperar o goblin agir")


@register_event("skeleton")
class Skeleton(Event):
    title = "Esqueleto"

    description = (
        "Um esqueleto aparece para te atacar,"
        "Você saca sua arma e se prepara."
    )

    def run(self, player):
        print(self.description)
        print("1 - Atacar primeiro")
        print("2 - Esperar o esqueleto agir")


@register_event("bandit")
class Bandit(Event):
    title = "Bandido"

    description = (
        "Um bandido surge para te atacar,"
        "Você saca sua arma e se prepara."
    )

    def run(self, player):
        print(self.description)
        print("1 - Atacar primeiro")
        print("2 - Esperar o bandido atacar")
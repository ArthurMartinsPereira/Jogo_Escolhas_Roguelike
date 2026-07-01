from Events.base import Event
from Events.registry import register_event

@register_event("small_treasure_chest")
class SmallTreasureChest(Event):

    title = "Pequeno Baú do Tesouro"

    description = (
        "Enquanto você passava por algumas velhas ruínas, você"
        "encontra um um pequeno baú trancado ao lado de uma velha"
        "estátua."
    )

    def run(self, player):

        print(self.description)

        print("1 - Forçar o baú a abrir.(str%)")
        print("2 - Usar uma gazula para abrir.(spd%)")
        print("3 - Lançar o feitiço de Chave Mágica.(Stamina -1)")
        print("4 - Ignorar.")

@register_event("treasure_chest")
class TreasureChest(Event):

    title = "Baú do Tesouro"

    description = (
        "Enquanto você passeava por uma praia você nota um"
        "um velho baú trancado meio enterrado na areia."
    )

    def run(self, player):

        print(self.description)

        print("1 - Forçar o baú a abrir.(str%)")
        print("2 - Usar uma gazula para abrir.(spd%)")
        print("3 - Lançar o feitiço de destrancar.(Stamina -1)")
        print("4 - Ignorar.")

@register_event("regal_treasure_chest")
class RegalTreasureChest(Event):

    title = "Belo Baú do Tesouro"

    description = (
        "Após um tempo caminhando uma densa neblina surge e você "
        "acaba se perdendo. Então na sua frente um enorme baú"
        "decorado aparece através da neblina"

    )

    def run(self, player):

        print(self.description)

        print("1 - Tentar destravar o mecanismo de tranca.(int%)")
        print("2 - Tentar forçar a tranca.(str%)")
        print("3 - Usar sua percepção para encontrar pistas(spd%)")
        print("4 - Ignorar.")
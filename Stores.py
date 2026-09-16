from Combat.Items.registry import create_item


class Store:

    def __init__(self, items):
        self.items = []

        for item_name in items:
            self.items.append(create_item(item_name))

    def show(self, player):

        while True:

            print("\n=== LOJA ===")
            print(f"Ouro: {self.player.gold}")

            for i, item in enumerate(self.items, start=1):
                print(
                    f"{i} - {item.name} "
                    f"({item.rarity}) "
                    f"- {item.value} moedas"
                )

            print("0 - Sair")

            choice = input("> ")

            if choice == "0":
                break

            try:
                index = int(choice) - 1
                item = self.items[index]

            except (ValueError, IndexError):
                print("Escolha inválida.")
                continue

            self.buy(item)

    def buy(self, item):

        if self.player.gold < item.value:
            print("Você não possui moedas suficientes.")
            return

        self.player.gold -= item.value
        self.player.add_item(item)

        print(
            f"Você comprou {item.name} "
            f"por {item.value} moedas."
        )
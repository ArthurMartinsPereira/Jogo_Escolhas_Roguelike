from Events.Stores_Base import Store


class StoreInterface:

    def __init__(self, store):
        self.store = store

    def show(self, player):

        while True:

            print("\n=== LOJA ===")
            print(f"Ouro: {player.gold}")

            if not self.store.items:
                print("A loja está vazia.")
            else:
                for i, item in enumerate(
                    self.store.items,
                    start=1
                ):
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
                item = self.store.items[index]

            except (ValueError, IndexError):
                print("Escolha inválida.")
                continue

            self.buy(player, item)

    def buy(self, player, item):

        if player.gold < item.value:
            print("Você não possui moedas suficientes.")
            return

        player.gold -= item.value
        player.add_item(item)

        print(
            f"Você comprou {item.name} "
            f"por {item.value} moedas."
        )

    def sell(self, player, item):

        price = self.store.get_sell_price(player, item)

        player.remove_item(item)
        player.gold += price

        print(
            f"Você vendeu {item.name} "
            f"por {price} moedas."
        )
from Combat.Items.registry import create_item
from Events.Stores_Base import Store
from Events.Stores_Interface import StoreInterface
from player import Player


player = Player("Teste")

print(f"Nível: {player.level}")
print(f"Ouro inicial: {player.gold}")

store = Store([
    "iron_sword",
    "iron_armor"
])

store.generate_stock(player)

interface = StoreInterface(store)
interface.show(player)

print("\n=== RESULTADO ===")
print(f"Ouro: {player.gold}")

player.show_inventory()
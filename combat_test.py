from player import Player
from Combat.Enemies.registry import create_enemy

player = Player("Arthur")
enemy = create_enemy("wolf")

round_num = 1

while player.hp > 0 and enemy.hp > 0:

    print(f"\n--- Turno {round_num} ---")

    player.attack(enemy)

    print(
        f"{player.name}: {player.hp}/{player.max_hp}"
    )

    print(
        f"{enemy.name}: {enemy.hp}/{enemy.max_hp}"
    )

    if enemy.hp <= 0:
        break

    enemy.attack(player)

    print(
        f"{player.name}: {player.hp}/{player.max_hp}"
    )

    print(
        f"{enemy.name}: {enemy.hp}/{enemy.max_hp}"
    )

    round_num += 1

print("\nFim da batalha")
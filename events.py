import random
from combat import Enemy, battle


def random_event(player):
    roll = random.randint(1, 3)

    if roll == 1:
        print("You found a treasure chest!")
        player.gold += 30

    elif roll == 2:
        enemy = Enemy("Goblin", 30, 5)
        battle(player, enemy)

    elif roll == 3:
        print("You find a place to rest and recover...")
        player.life += 1
        player.stamina += 1


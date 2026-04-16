import random


class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0


def attack(attacker, defender):
    dmg = random.randint(5, 10)

    defender.hp -= dmg
    print(f"{attacker} deals {dmg} damage!")


def battle(player, enemy):
    print(f"A {enemy.name} apears in your way...")
    player.hp = player.calculate_hp()

    while player.hp > 0 and enemy.hp > 0:
        action = input("Attack or Run? ").lower()

        if action == "attack":
            attack("Player", enemy)
            if enemy.is_alive():
                attack(enemy.name, player)
        else:
            print("You escaped!")
            return

    if player.hp <= 0:
        player.life = 0
        print("You died...")
    else:
        print("Enemy defeated!")
        player.xp += 1

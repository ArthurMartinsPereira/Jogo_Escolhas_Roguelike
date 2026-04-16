from player import Player
from events import random_event


def game_loop():
    player = Player()

    while player.is_alive():
        print("---New Event---")
        random_event(player)

        print(f"Lives: {player.life}| Stamina: {player.stamina}")

        if player.xp >= 20:
            player.level_up()

    print("Game Over")


if __name__ == "__main__":
    game_loop()
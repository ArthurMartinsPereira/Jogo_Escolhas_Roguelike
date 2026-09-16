from player import Player
from Combat.Enemies.registry import create_enemy
from Combat.battle import Battle

player = Player("Arthur")

enemy = create_enemy("necromancer")

battle = Battle(
    player,
    enemy
)

battle.start()
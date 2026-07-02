import Events
from player import Player
from Events.event_manager import EventManager

player = Player("Arthur")

events = EventManager()

while player.has_lives():

    events.run_random_event(player)

    input("\nPressione ENTER para continuar...")
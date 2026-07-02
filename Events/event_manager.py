import random
from Events.registry import EVENTS, create_event

class EventManager:
    def __init__(self):
        pass

    def available_events(self, player):
        available = []
        for name, event_cls in EVENTS.items():
            if getattr(event_cls, "unique", False) and name in player.completed_events:
                continue
            available.append(name)

        return available

    def random_event(self, player):
        events = self.available_events(player)

        if not events:
            return None

        name = random.choice(events)
        return create_event(name)

    def run_random_event(self, player):
        event = self.random_event(player)

        if not event:
            print("Nenhum evento disponível.")
            return

        event.run(player)

        if event.unique:
            player.completed_events.add(event.id)

EVENTS = {}

def register_event(name):

    def wrapper(cls):

        EVENTS[name] = cls

        return cls

    return wrapper

def create_event(name):

    if name not in EVENTS:
        raise ValueError(
            f"Evento '{name}' não existe!"
        )

    event = EVENTS[name]()
    event.id = name

    return event
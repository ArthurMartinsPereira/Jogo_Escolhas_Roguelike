ENEMIES = {}


def register_enemy(name):
    def wrapper(cls):
        ENEMIES[name] = cls
        return cls

    return wrapper


def create_enemy(name):
    if name not in ENEMIES:
        raise ValueError(
            f"Enemy '{name}' não existe!"
        )

    return ENEMIES[name]()
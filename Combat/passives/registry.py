PASSIVES = {}
MAX_PASSIVE_LEVEL = 4


def register_passive(name, description="", value_func=None, priority=0, max_level=MAX_PASSIVE_LEVEL):
    def wrapper(func):
        PASSIVES[name] = {
            "func": func,
            "description": description,
            "value_func": value_func,
            "priority": priority,
            "max_level": max_level
        }
        return func
    return wrapper

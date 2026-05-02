ITEMS = {}


def register_item(name):
    def wrapper(cls):
        ITEMS[name] = cls
        return cls
    return wrapper


def create_item(name):
    if name not in ITEMS:
        raise ValueError(f"Item '{name}' não existe!")
    return ITEMS[name]()


import Menu


class Submenu(Menu.Menu):
    def __init__(self, func, **kwargs):
        super().__init__(kwargs.get("label") or func.__name__)
        self.func = func
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self, *args, **kwargs):
        self.func(self, *args, **kwargs)


def submenu(label=None, **attrs):
    def decorator(func):
        if isinstance(func, Submenu):
            raise TypeError('Func is already a submenu.')
        return Submenu(func, label=label, **attrs)

    return decorator
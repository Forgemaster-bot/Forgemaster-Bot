import Submenu

import Submenu

# class Menu:
#     def __init__(self, label=None, func, *args, **kwargs):
#         self.func = func
#         self.label = kwargs.get("label") or func.__name__
#         self.all_subitems = {}
#
#         if self.label is None:
#             raise AttributeError("Invalid label passed")
#
#         for k, v in kwargs.items():
#             setattr(self, k, v)
#
#     def add_subitem(self, subitem):
#         print("add_subitem called")
#         if not isinstance(subitem, Menu):
#             raise TypeError('The subitem passed must be a subclass of MenuItemCommon')
#
#         if isinstance(self, Menu):
#             subitem.parent = self
#
#         if subitem.label in self.all_subitems:
#             raise RuntimeError(f"subitem already registered: {subitem.label}")
#
#         self.all_subitems[subitem.label] = subitem
#
#     def subitem(self, cls=None, *args, **kwargs):
#         def decorator(func):
#             kwargs.setdefault('parent', self)
#             result = subitem(cls=cls, *args, **kwargs)(func)
#             self.add_subitem(result)
#             return result
#         return decorator
#
#     def __call__(self, *args, **kwargs):
#         self.func(*args, **kwargs)
#
#
# def subitem(label=None, cls=None, **attrs):
#     if cls is None:
#         cls = Menu
#
#     def decorator(func):
#         if isinstance(func, Menu):
#             raise TypeError('Func is already a subitem.')
#         return cls(func, label=label, **attrs)
#
#     return decorator
#


class Menu:
    def __init__(self, label, **kwargs):
        self.all_submenus = {}
        self.label = kwargs.get("label")

    def add_submenu(self, submenu):
        print("add_submenu called")
        if not isinstance(submenu, Submenu.Submenu):
            raise TypeError('The submenu passed must be a subclass of Submenu')

        if isinstance(self, Submenu.Submenu):
            submenu.parent = self

        if submenu.label in self.all_submenus:
            raise RuntimeError(f"Submenu already registered: {submenu.label}")

        self.all_submenus[submenu.label] = submenu

    def submenu(self, *args, **kwargs):
        def decorator(func):
            kwargs.setdefault('parent', self)
            result = Submenu.submenu(*args, **kwargs)(func)
            self.add_submenu(result)
            return result
        return decorator

    def select_submenus(self):
        for i, key in enumerate(self.all_submenus.keys(), 1):
            print(f"{i} : {key}")
            print(f"Opening '{key}'")
            self.all_submenus[key]()


# class Submenu(Menu.Menu):
#     def __init__(self, func, **kwargs):
#         super().__init__()
#         self.func = func
#
#         for k, v in kwargs.items():
#             setattr(self, k, v)
#
#     def __call__(self, *args, **kwargs):
#         self.func(*args, **kwargs)
#
#
# # def submenu(label=None, **attrs):
# #     def decorator(func):
# #         if isinstance(func, Submenu):
# #             raise TypeError('Func is already a submenu.')
# #         return Submenu(func, label=label, **attrs)
# #
# #     return decorator
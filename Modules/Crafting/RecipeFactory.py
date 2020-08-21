import random


class Recipe:
    def __init__(self, **kwargs):
        self.prefix = None
        self.cost = None
        self.type = None
        self.outcomes = None
        self.pre_crafting_steps = []
        self.amount = 1
        for key, value in kwargs.items():
            setattr(self, key, value)

    def can_afford(self, character):
        return character.has_item_quantity_by_keyword(**self.cost)

    def craft(self, character):
        self.__remove_costs(character)
        if not all([check(self, character) for check in self.pre_crafting_steps]):
            return None
        item_crafted = self.__create_item()
        character.modify_item_amount(item_crafted, 1)
        return item_crafted
        
    def __remove_costs(self, character):
        for k, v in self.cost.items():
            character.remove_item_amount(k, v)

    def __create_item(self):
        return "{} {}".format(self.prefix, random.sample(self.outcomes, 1)[0])

    def __str__(self):
        return "{} - {}".format(self.name, ", ".join("{}:{}".format(k, v) for k, v in self.cost.items()))


def not_implemented(recipe, character):
    raise NotImplementedError("type not implemented")


def create_recipe(data: dict) -> Recipe:
    lookup_table = {
        'dc': (lambda r, c: not_implemented(r, c))
    }

    recipe = Recipe(**data)
    if 'type' in data:
        for item in data['type']:
            if item in lookup_table:
                recipe.pre_crafting_steps.append(lookup_table[item])
            else:
                raise ValueError("item[{}] not in lookup_table".format(item))
    return recipe


# import Character.Character
# import Crafting.Parser
# character = Character.Character.Character("E4CEFA15-B3C7-4B6E-8EA9-DC140B5D0338")
# data = Crafting.Parser.parse_crafting_file()
# recipe = Crafting.Parser.ask_user_to_select_recipe(None, None, data)
# if recipe.can_afford(character):
#     recipe.craft(character)
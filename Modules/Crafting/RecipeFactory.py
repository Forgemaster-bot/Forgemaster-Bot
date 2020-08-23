import random

class RecipeResult:
    def __init__(self, result, message):
        self.result = result
        self.message = message

class Recipe:
    def __init__(self, **kwargs):
        """
        Initializes recipe object and overrides default values based on keyword arguments passed.
        :param kwargs: Keyword:value pairs for setting attributes.

        Possible attributes:
            - prefix = String prefix for crafted item.
            - cost = Dictionary containing item costs.
            - type = Type used by factory for determining pre_crafting_steps.
            - pre_crafting_steps = List of functions to call and check before creating item and giving to player.
                                   If any of these return 'False', then the item is not crafted but costs are removed.
            - amount = Quantity of item to make. Default: 1
        """
        self.amount = 1
        self.cost = None
        self.outcomes = None
        self.prefix = None
        self.prereq = None
        self.special = None
        self.special_steps = []

        for key, value in kwargs.items():
            setattr(self, key, value)

    def can_afford(self, character) -> bool:
        """
        Check if character can afford the costs of this recipe.
        :param character: object which has 'has_item_quantity_by_keyword' function
        :return: bool
        """
        return character.has_item_quantity_by_keyword(**self.cost)

    def craft(self, character) -> RecipeResult:
        """
        Crafts item for player. First it removes the costs of the recipe from the player, then if all pre_crafting_steps
        return 'True' it will create the item and update the character.
        :param character: Object which holds items and has 'remove_item_amount' and 'modify_item_amount' functions.
        :return: String name of the item crafted
        """
        special_step_result = [step.execute(self, character) for step in self.special_steps]
        self.__remove_costs(character)
        for step in special_step_result:
            if not step.result:
                return step
        item_crafted = self.__create_item()
        character.modify_item_amount(item_crafted, 1)
        return RecipeResult(True, item_crafted)
        
    def __remove_costs(self, character) -> None:
        """
        Removes v num of k named items from player, where k:v are in the costs of this recipe.
        :param character: Object which has 'remove_item_amount' function.
        :return: None
        """
        for k, v in self.cost.items():
            character.remove_item_amount(k, v)

    def __create_item(self) -> str:
        """
        Returns item name by randomly selecting an outcome and prefixing it with prefix attribute.
        :return: str - item name
        """
        outcome = random.sample(self.outcomes, 1)[0]
        return " ".join(item for item in [self.prefix, outcome] if item)

    def formatted_name(self):
        """
        Returns formatted and labelled recipe name
        :return: str
        """
        return "**Name:** {}".format(self.name)

    def formatted_costs(self):
        """
        Returns formatted and labelled recipe costs
        :return:
        """
        return "**Costs:** {}".format(", ".join(f"{k}:{v}" for k, v in self.cost.items()))

    def formatted_special_steps(self):
        return "-".join(f"{str(step)}" for step in self.special_steps)

    def __str__(self):
        """
        Formats recipe as a string of format '<name> - <cost name>:<cost quantity>...'
        :return: string of recipe name and costs
        """
        return f"{self.formatted_name()} - {self.formatted_costs()} - {self.formatted_special_steps()}"


def not_implemented(recipe: Recipe, character) -> None:
    """
    Helper function which returns NotImplementedError. Used for crafting if unknown type has been declared.
    :param recipe: Recipe object
    :param character: object which is crafting an item
    :return: None
    """
    raise NotImplementedError("type not implemented")


class DifficultyClassCheckStep:
    def __init__(self):
        self.fields = ['die', 'mod', 'dc']

    def validate_fields(self, recipe: Recipe):
        dc_check_dict = recipe.special['dc check']
        # Check that fields exist
        for option in self.fields:
            if option not in dc_check_dict:
                raise ValueError(f"dc check field {option} missing for {str(recipe)}")
            else:
                option_value = dc_check_dict[option]
                try:
                    setattr(self, option, int(option_value))
                except ValueError as err:
                    raise ValueError(f"Non-integer value '{option_value}' in field {option} for {str(recipe)}")
        return self

    def execute(self, recipe: Recipe, character) -> RecipeResult:
        roll = random.randint(1, self.die)
        result = (roll + self.mod) >= self.dc
        message = "" if result else f"DC not met. Roll={roll}; Mod={self.mod}; DC={self.dc};"
        return RecipeResult(result, message)

    def __str__(self):
        sign = ["", "+"][self.mod > 0]
        return f"Must meet **DC[{self.dc}]** rolling a **d{self.die}** with **{sign}{self.mod}** modifier."


class RandomAmountStep:
    def __init__(self):
        self.fields = ['die', 'mod']

    def validate_fields(self, recipe: Recipe):
        dc_check_dict = recipe.special['random amount']
        # Check that fields exist
        for option in self.fields:
            if option not in dc_check_dict:
                raise ValueError(f"'random amount' field {option} missing for {str(recipe)}")
            else:
                option_value = dc_check_dict[option]
                try:
                    setattr(self, option, int(option_value))
                except ValueError as err:
                    raise ValueError(f"Non-integer value '{option_value}' in field {option} for {str(recipe)}")
        return self

    def execute(self, recipe: Recipe, character) -> RecipeResult:
        recipe.amount = random.randint(1, self.die) + self.mod
        return RecipeResult(True, "")

    def __str__(self):
        sign = ["", "+"][self.mod > 0]
        return f"Amount created is determined by rolling a **d{self.die}** with **{sign}{self.mod}** modifier."


lookup_table = {
    'dc check': DifficultyClassCheckStep,
    'random amount': RandomAmountStep
}


def create_recipe(data: dict) -> Recipe:
    """
    Factory method for creating a Recipe object based on recipe defined in yaml config.
    This factory will specialize the created Recipe based on the types found in the data.
    :param data: Recipe dictionary
    :return: Specialized Recipe object
    """
    recipe = Recipe(**data)
    if 'special' in data:
        for item in data['special']:
            if item in lookup_table:
                special_obj = lookup_table[item]()
                special_obj.validate_fields(recipe)
                recipe.special_steps.append(special_obj)
            else:
                raise ValueError(f"'type' of '{item}' not in lookup_table")
    return recipe


# import Character.Character
# import Crafting.Parser
# character = Character.Character.Character("E4CEFA15-B3C7-4B6E-8EA9-DC140B5D0338")
# data = Crafting.Parser.parse_crafting_file()
# recipe = Crafting.Parser.ask_user_to_select_recipe(None, None, data)
# if recipe.can_afford(character):
#     recipe.craft(character)

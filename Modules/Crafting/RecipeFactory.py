# TODO: Cleanup validate_special_field functions. These can definitely be refactored into a lookup table.
import random
import types
# from itertools import chain


def flatten(S):
    if not S:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


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

        result_message = ""
        for step in special_step_result:
            if not step.result:
                return step
            if step.message is not None:
                result_message = f"{result_message}\n{step.message}"

        item_crafted = self.__create_item()
        character.modify_item_amount(item_crafted, self.amount)

        result_message = f"{result_message}\nYou successfully crafted **{self.amount}x[{item_crafted}]**"
        return RecipeResult(True, result_message)
        
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
        flattened_outcomes = flatten(self.outcomes)
        outcome = random.sample(flattened_outcomes, 1)[0]
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


def validate_special_field_int(step, data: dict, key, recipe):
    if key not in data:
        raise ValueError(f"'{step.step_label}' field {key} missing for {str(recipe)}")
    value = data[key]
    try:
        setattr(step, key, int(value))
    except ValueError as err:
        raise ValueError(f"Non-integer value '{value}' in step '{step.step_label}' and field '{key}' for {str(recipe)}")


def validate_special_field_bool(step, data: dict, key, recipe):
    if key not in data:
        raise ValueError(f"'{step.step_label}' field {key} missing for {str(recipe)}")
    value = data[key]
    try:
        setattr(step, key, bool(value))
    except ValueError as err:
        raise ValueError(f"Non-boolean value '{value}' in step '{step.step_label}' and field '{key}' for {str(recipe)}")


def validate_special_field_str(step, data: dict, key, recipe):
    if key not in data:
        raise ValueError(f"'{step.step_label}' field {key} missing for {str(recipe)}")
    value = data[key]
    if isinstance(value, str):
        setattr(step, key, value)
    else:
        raise ValueError(f"Non-string value '{value}' in step '{step.step_label}' and field '{key}' for {str(recipe)}")


def validate_special_field_dict(step, data: dict, key, recipe):
    if key not in data:
        raise ValueError(f"'{step.step_label}' field {key} missing for {str(recipe)}")
    value = data[key]
    if value is None or isinstance(value, dict):
        setattr(step, key, value)
    else:
        raise ValueError(f"Non-dict value '{value}' in step '{step.step_label}' and field '{key}' for {str(recipe)}")


def validate_special_field_list(step, data: dict, key, recipe):
    if key not in data:
        raise ValueError(f"'{step.step_label}' field {key} missing for {str(recipe)}")
    value = data[key]
    if value is None or isinstance(value, list):
        setattr(step, key, value)
    else:
        raise ValueError(f"Non-list value '{value}' in step '{step.step_label}' and field '{key}' for {str(recipe)}")


class DifficultyClassCheckStep:

    step_label = 'dc check'

    def __init__(self):
        self.fields = ['die', 'mod', 'dc']

    def validate_fields(self, recipe: Recipe):
        data_dict = recipe.special['dc check']
        # Check that fields exist
        for option in self.fields:
            validate_special_field_int(self, data_dict, option, recipe)
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
    """
    Randomizes amount of items made in recipe. `recipe.amount` is set to random number between [1..`die`]+`mod`

    random amount:
        die: <int>
        mod: <int>
    """

    step_label = 'random amount'

    def __init__(self):
        self.fields = ['die', 'mod']

    def validate_fields(self, recipe: Recipe):
        data_dict = recipe.special['random amount']
        # Check that fields exist
        for option in self.fields:
            validate_special_field_int(self, data_dict, option, recipe)
        return self

    def execute(self, recipe: Recipe, character) -> RecipeResult:
        recipe.amount = random.randint(1, self.die) + self.mod
        return RecipeResult(True, "")

    def __str__(self):
        sign = ["", "+"][self.mod > 0]
        return f"Amount created is determined by rolling a **d{self.die}** with **{sign}{self.mod}** modifier."


class RandomOutcomeStep:
    """
    Randomizes outcome list in recipe. Rolls die, finds matching range, and replaces recipe outcomes with those given.

    random outcome:
      die: <int>
      ranges:
        - label: <str>
          start: <int>
          stop: <int>
          outcomes: <list>
          [step: <int>] # optional
        - {label: <str>, start: <int>, stop: <int>: outcomes: <list>}
    """

    step_label = 'random outcome'

    def __init__(self):
        self.field_label_die = 'die'
        self.field_label_ranges = 'ranges'
        self.field_label_ranges_label = 'label'
        self.field_label_ranges_start = 'start'
        self.field_label_ranges_stop = 'stop'
        self.field_label_ranges_outcomes = 'outcomes'
        # Optional fields
        self.field_label_ranges_step = 'step'
        self.field_label_ranges_original = 'original'
        # Default init dictionary
        self.range_dict = {}

    def validate_fields(self, recipe: Recipe):
        data_dict = recipe.special[self.step_label]
        validate_special_field_int(self, data_dict, self.field_label_die, recipe)
        validate_special_field_dict(self, data_dict, self.field_label_ranges, recipe)
        for item in data_dict[self.field_label_ranges].values():
            if not isinstance(item, dict):
                raise ValueError(f"Invalid '{self.field_label_ranges}' item '{item}' for {str(recipe)}")
            # Create temporary namespace for hold range information
            range_container = types.SimpleNamespace()
            range_container.step_label = f'{self.step_label}:{self.field_label_ranges}'
            range_container.step = 1
            # Validate fields in range and assign them to the temporary namespace
            validate_special_field_str(range_container, item, self.field_label_ranges_label, recipe)
            validate_special_field_int(range_container, item, self.field_label_ranges_start, recipe)
            validate_special_field_int(range_container, item, self.field_label_ranges_stop, recipe)

            # Validate optional fields
            if self.field_label_ranges_step in item:
                validate_special_field_int(range_container, item, self.field_label_ranges_step, recipe)
            if self.field_label_ranges_outcomes in item:
                validate_special_field_list(range_container, item, self.field_label_ranges_outcomes, recipe)
            if (self.field_label_ranges_original in item) and (item[self.field_label_ranges_original] is True):
                range_container.outcomes = recipe.outcomes

            # Create range from namespace and assign to range_dict with range as key namespace obj as value
            range_key = range(range_container.start, range_container.stop+1, range_container.step)
            self.range_dict[range_key] = range_container
        return self

    def execute(self, recipe: Recipe, character) -> RecipeResult:
        roll = random.randint(1, self.die)
        valid_ranges = [self.range_dict[key] for key in self.range_dict if roll in key]

        # Handle error cases
        if len(valid_ranges) == 0:
            return RecipeResult(False, f"Valid range not found for roll '{roll}'!")
        elif len(valid_ranges) > 1:
            return RecipeResult(False, f"Multiple ranges found for '{roll}'!")

        # Handle unchanged, and intended failure conditions
        range_container = valid_ranges[0]
        result_message = f"You rolled '{roll}'. {range_container.label}"

        # Fail crafting if outcome indicates no item should be crafted
        if range_container.outcomes is None:
            return RecipeResult(False, result_message)

        # Successfully update recipe outcomes
        recipe.outcomes = range_container.outcomes
        return RecipeResult(True, result_message)

    def __str__(self):
        return f"Outcomes are determined by rolling a **d{self.die}**."


lookup_table = {
    'dc check': DifficultyClassCheckStep,
    'random amount': RandomAmountStep,
    'random outcome': RandomOutcomeStep
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

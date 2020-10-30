from cogs.utils import menu as Menu
from cogs.utils import textmenus
from cogs.utils import StandaloneQueries
import Crafting.Parser as Parser
import Crafting.RecipeFactory as RecipeFactory
import Crafting.Crafting as Crafting
import itertools
import logging
import asyncio
import discord
import math
from discord.ext import commands
import Exceptions
import Connections
import Update_Google_Roster as Roster

log = logging.getLogger(__name__)

class RecipeSelectionMenu(Menu.BaseCharacterMenu):
    title = "Recipe Crafting - Select Recipe"

    def __init__(self, label: str, data: list, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        for item in data:
            if not isinstance(item, dict):
                raise RuntimeError("Data passed expected to be list of recipes...Got list containing non-dict items.")
            self.submenu(label=item['name'])(self.make_recipe_confirm(item))

    def get_initial_message(self):
        return f"Please select one of the **{self.label}** recipes you would like to craft."

    async def on_confirm(self, recipe):
        if recipe.can_afford(self.character) is False:
            channel = await Menu.get_dm_channel(self.ctx.author)
            return await channel.send(f"You cannot afford this recipe: '{str(recipe)}'")
        await Crafting.craft_recipe(self.ctx, self.character, recipe)

    @staticmethod
    def make_recipe_confirm(data: dict):
        async def recipe_confirm(menu, payload):
            recipe = RecipeFactory.create_recipe(data)
            msg = f"Would you like to craft this recipe?"
            embed_info = Menu.BaseMenu.create_embed_info()
            embed_fields = [
                textmenus.EmbedInfo.Field('Recipe', recipe.name),
                textmenus.EmbedInfo.Field('Costs', recipe.list_costs()),
                textmenus.EmbedInfo.Field('Special', recipe.list_special_steps())
            ]
            embed_info.fields.extend(embed_fields)
            m = await Menu.start_menu(menu.ctx, Menu.ConfirmMenu, message=msg, embed_info=embed_info)
            if m.confirm:
                await menu.on_confirm(recipe)
        return recipe_confirm


class RecipeCategoryMenu(Menu.BaseCharacterMenu):

    def __init__(self, label: str, data: dict, **kwargs):
        super().__init__(**kwargs, title=f"Recipe Crafting - {label} Options")
        self.label = label

        if not isinstance(data, dict):
            raise RuntimeError("Data is not a dictionary")

        for key, value in data.items():
            if isinstance(value, dict):
                self.submenu(label=key)(self.make_query_category_options(key, value))
            elif isinstance(value, list):
                self.submenu(label=key)(self.make_query_recipe_selection(key, value))

    def get_initial_message(self):
        return f"If you would like to view more, please select one of the following **{self.label}** options."

    @staticmethod
    def make_query_category_options(label: str, data: dict):
        async def query_category_options(menu, payload):
            await Menu.start_menu(menu.ctx, RecipeCategoryMenu, character=menu.character, data=data, label=label)
        return query_category_options

    @staticmethod
    def make_query_recipe_selection(label: str, data: list):
        async def query_recipe_selection(menu, payload):
            await Menu.start_menu(menu.ctx, RecipeSelectionMenu, character=menu.character, data=data, label=label)
        return query_recipe_selection


async def open_file_based_recipe_menu(ctx, label: str, character):
    available_selections = Parser.get_parsed_data(label)['recipes']
    await Menu.start_menu(ctx, RecipeCategoryMenu, character=character, data=available_selections, label=label)

def make_skill_choice_func(skill):
    async def choice_func(menu, payload):
        tool = StandaloneQueries.select_tool(skill.name)
        if not menu.character.has_item(tool):
            log.info(f"skill_choice_func - {menu.character.info.name} - Does not have '{tool}'")
            await menu.channel.send(f"You do not have the required tool to craft: '{tool}'.")
        else:
            # await Menu.start_menu(menu.ctx, menu.next_menu, character=menu.character, skill=skill)
            await menu.next_menu(menu, skill)
    return choice_func

def make_choice_func(skill):
    async def choice_func(menu, payload):
        await menu.next_menu(menu, skill)
    return choice_func

async def ask_for_quantity(ctx: commands.Context, max_num: int) -> int:
    channel = await Menu.get_channel(ctx)

    def wait_for_integer(message: discord.Message):
        try:
            if ctx.author.id != message.author.id or channel.id != message.channel.id:
                return False
            content = message.content.lower()
            if content == 'stop' or content == 'exit':
                return True
            value = int(message.content)
            if value < 0 or value > max_num:
                # await message.author.send(f"Must be between 0 and {max_num}, 'stop', or 'exit. Please try again.")
                return False
            return True
        except ValueError:
            # await message.author.send(f"Must be between 0 and {max_num}, 'stop', or 'exit. Please try again.")
            return False

    await channel.send(f"How many would you like to craft? You may craft up to {max_num}. "
                           f"[Please input an integer value between 0 and {max_num}, 'stop', or 'exit']")
    try:
        msg = await ctx.bot.wait_for('message', check=wait_for_integer, timeout=30)
        return int(msg.content)
    except asyncio.TimeoutError:
        await channel.send(f"Timed out, aborting...")
        raise Exceptions.StopException
    except ValueError:
        await channel.send(f"Invalid number, aborting...")
        raise Exceptions.StopException

async def craft_item_selection(menu, choice):
    log.info(f"craft_item_selection - {menu.character.info.name} - User selected {choice} ")
    choice.Value = choice.Value / 2  # Modify value to be half its value for the crafting cost

    # Determine quantity and total cost based on player input
    crafting_limit = StandaloneQueries.fetch_crafting_limit_row(menu.character.id).Crafting_Value
    max_num = math.floor(min(menu.character.get_gold(), crafting_limit) / choice.Value)
    quantity = await ask_for_quantity(menu.ctx, max_num)
    total_cost = choice.Value * quantity

    log.info(f"craft_item_selection - {menu.character.info.name} - Crafting limit is {max_num}. User chose {quantity}."
             f"Crafting cost will be {total_cost}")

    # Check if player has enough gold to cover this total cost
    if not menu.character.has_item_quantity_by_keyword(Gold=total_cost):
        menu.channel.send(f"Unfortunately, you do not have enough gold. This item costs '**{choice.Value}gp**' to craft.")
        log.info(f"craft_item_selection - {menu.character.info.name} - User did not have enough gold.")
        return

    # Query user and update limit, gold, and items if sele
    new_limit = 0 if total_cost >= crafting_limit else crafting_limit - total_cost
    message = f"Would you like to craft **{quantity}x[{choice.Name}]** for a total of **{choice.Value} gp**?\n" \
              f"Your new crafting limit for the week will be: {new_limit}"
    m = Menu.ConfirmMenu(message)
    await m.start(menu.ctx, channel=menu.channel, wait=True)
    if m.confirm:
        menu.character.remove_item_amount('Gold', total_cost)
        menu.character.modify_item_amount(choice.Name, quantity)
        StandaloneQueries.update_crafting_value(menu.character.info.character_id, new_limit)
        msg = f"{menu.character.name} successfully crafted {quantity}x**{choice.Name}** for **{total_cost:.2f}gp**!"
        log.info(f"{msg} Original limit={crafting_limit}; New limit={new_limit};")
        await menu.channel.send(msg)
        await Connections.log_to_discord(menu.ctx, msg)
        Roster.update_character_in_roster(menu.character)

async def item_selection_menu(menu, choice):
    log.info(f"item_selection_menu - {menu.character.info.name} - User selected {choice} ")
    items = {item.Name: item for item in choice}
    message = f"Please select one of the following items to craft:"
    await Menu.start_menu(menu.ctx, Menu.ListCharacterMenu, character=menu.character, closure_func=make_choice_func,
                          message=message, next_menu=craft_item_selection, choices=items, title='Item Selection Menu')

async def item_type_menu(menu, choice):
    log.info(f"item_type_menu - {menu.character.info.name} - User selected {choice} ")
    data = StandaloneQueries.get_items_by_profession_and_cost(choice.name, menu.character.get_gold())
    grouped_data_by_type = {}
    for k, g in itertools.groupby(data, lambda item_info: item_info.data):
        grouped_data_by_type[k] = [item for item in g]
    message = f"Please select one of the item types for crafting:"
    await Menu.start_menu(menu.ctx, Menu.ListCharacterMenu, character=menu.character, closure_func=make_choice_func,
                          message=message, next_menu=item_selection_menu, choices=grouped_data_by_type,
                          title='Type Menu')


async def mundane_crafting_menu(ctx, character):
    message = f"Please choose one of the following skills for mundane crafting:"
    choices = character.get_skills_dict()
    if len(choices) == 0:
        channel = await Menu.get_channel(ctx)
        channel.send("Unfortunately, I do not have any available choices for this menu.")
        return
    await Menu.start_menu(ctx, Menu.ListCharacterMenu, character=character, closure_func=make_skill_choice_func,
                          message=message, next_menu=item_type_menu, choices=choices, title='Skill Menu')

# crafting_limit



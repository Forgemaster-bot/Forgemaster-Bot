import Crafting.Parser
import Crafting.Utils


async def craft_item_menu(cog, context, character, file_label):
    """
    Queries
    :param cog: discord cog object
    :param context: discord context object for client
    :param character: character object
    :param file_label: name portion of filename
    :return: None
    """
    try:
        data = Crafting.Parser.parse_file(file_label)
        recipe = await Crafting.Utils.ask_user_to_select_recipe(cog, context, data, file_label)
        if await Crafting.Utils.verify_prerequisites(context, character, recipe):
            if await Crafting.Utils.recipe_confirm(cog, context, recipe):
                await craft_recipe(cog, context, character, recipe)
    except FileNotFoundError as err:
        await Crafting.Utils.send_message(context, f"{file_label}.yml not found. Contact mod or admin.")
    await Crafting.Utils.send_message(context, "Returning to menu.")
    return


async def craft_recipe(cog, context, character, recipe):
    if recipe.can_afford(character):
        recipe_result = recipe.craft(character)
        if recipe_result.result:
            message = f"You successfully crafted **{recipe.amount}x[{recipe_result.message}]**"
            await Crafting.Utils.send_message(context, message)
        else:
            await Crafting.Utils.send_message(context, f"**Crafting failed.** {recipe_result.message}")
    else:
        await Crafting.Utils.send_message(context, "**Error** You cannot afford to craft this item.")

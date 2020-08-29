import Crafting.Parser
import Crafting.Utils
import Connections
import Update_Google_Roster as Roster

data = Crafting.Parser.parse_file('thaumstyn')


async def craft_item_menu(context, character, file_label):
    """
    Queries
    :param context: discord context object for client
    :param character: character object
    :param file_label: name portion of filename
    :return: None
    """
    available_recipes = data['recipes']
    recipe = await Crafting.Utils.ask_user_to_select_recipe(context, available_recipes, file_label)
    if recipe is not None:
        if await Crafting.Utils.verify_prerequisites(context, character, recipe):
            if recipe.can_afford(character):
                if await Crafting.Utils.recipe_confirm(context, recipe):
                    character.refresh()
                    await craft_recipe(context, character, recipe)
            else:
                msg = f"**Error** You cannot afford to craft this recipe: {str(recipe)}"
                await Crafting.Utils.send_message(context, msg)

    await Crafting.Utils.send_message(context, "Returning to menu.")
    return


async def craft_recipe(context, character, recipe):
    craft_result = recipe.craft(character)
    message = f"{craft_result.message}" if craft_result.result else f"**Crafting failed.** {craft_result.message}"
    await Crafting.Utils.send_message(context, craft_result.prereq_message)
    await Crafting.Utils.send_message(context, message)
    log = f"{character.info.name} is crafting [{str(recipe)}] - {message.replace('You', character.info.name)}"
    await Connections.log_to_discord(context.cog, log)
    Roster.update_character_in_roster(character)




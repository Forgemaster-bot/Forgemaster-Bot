from Crafting.RecipeFactory import create_recipe
import asyncio


class StopException(Exception):
    """
    Exception used to stop a menu.
    TODO: Move into menu cogs.
    """
    pass


class ExitException(Exception):
    """
    Exception used to exit the '$menu' command.
    TODO: Move into menu cogs.
    """
    pass


async def send_message(context, message) -> None:
    """
    Helper for sending a message to user.
    :param context: discord context object
    :param message: message to send to user.
    :return: None
    """
    await context.message.author.send(message)
    # print(message)


def is_stop_response(response) -> None:
    """
    Helper function to check response and raise stop exception if needed.
    :param response: Message response from user.
    :return: None
    """
    if response.lower() == 'stop':
        raise StopException()


def is_exit_response(response):
    """
    Helper function to check response and raise exit exception if needed.
    :param response: Message response from user.
    :return: None
    """
    if response.lower() == 'exit':
        raise ExitException()


def is_stop_or_exit(response) -> False:
    """
    Helper function used to raise exit/stop exceptions if needed. Always returns False or raises exception.
    :param response: Message response from user.
    :return: False
    """
    is_stop_response(response)
    is_exit_response(response)
    return False


# responses = ["1", "1", "2"]
# async def wait_for_reply(cog, context):
#     return responses.pop()
async def wait_for_reply(cog, context) -> str:
    """
    Waits, gets, and returns user response. Raises ExitException on timeout.
    :param cog: discord cog object
    :param context: discord context object for client
    :return: String message response of user.
    """
    def check_reply(r):
        return r.author == context.author and r.channel.type[1] == 1
    try:
        msg = await cog.bot.wait_for('message', timeout=120.0, check=check_reply)
        return msg.content.lower()
    except asyncio.TimeoutError:
        raise ExitException()


async def get_reply(cog, context, question_dict) -> str:
    """
    Queries for reply from user until response matches key in question_dict.
    :param cog: discord cog object
    :param context: discord context object for client
    :param question_dict: dictionary/list of keys to check for
    :return: String message response of user which exists in question_dict.
    """
    response = ""
    while True:
        response = await wait_for_reply(cog, context)
        if (response in question_dict) or is_stop_or_exit(response):
            break
        else:
            message = f"'{response}' is invalid. Must be one of {question_dict.keys()}, 'stop', or 'exit'"
            await send_message(context, message)
    return response


def enumerate_keys(data: dict) -> dict:
    """
    Creates dictionary of enumerated keys from passed dictionary
    :param data: Dictionary with keys to enumerate
    :return: Enumerated dict
    """
    return {str(i): key for i, key in enumerate(data.keys(), start=1)}


def format_dict(data: dict) -> str:
    """
    Returns string of format "key : value" separated by new lines.
    :param data: dictionary to format
    :return: str
    """
    return "\n".join(f"{k} : {v}" for k, v in data.items())


async def query_user(cog, context, data: dict):
    """
    Converts data dictionary to set of numbers and queries user to select one. Once the user has selected an option,
    the corresponding key in data will be sent to user and returned to caller.
    :param cog: discord cog object
    :param context: discord context object for client
    :param data: data to query from user
    :return:
    """
    question_dict = enumerate_keys(data)
    await send_message(context, format_dict(question_dict))
    response = await get_reply(cog, context, question_dict)
    return question_dict[response]


async def query_until_recipe(cog, context, data, label):
    """
    Recursive function which will query user to select key in a dict until a non-dictionary value is found.
    When a key is selected, this function will be called until a non-dictionary value is returned by basecase.
    :param cog: discord cog object
    :param context: discord context object for client
    :param data: yaml file data containing recipes
    :param label: name of current category
    :return: non-dictionary value
    """
    if isinstance(data, dict):
        """
        Query user to select next dict to parse and recurse.
        """
        await send_message(context, f"Please select a category you would like to craft from **{label}**: ")
        next_key = await query_user(cog, context, data)
        return await query_until_recipe(cog, context, data[next_key], next_key)
    elif isinstance(data, list):
        """
        Parse recipe list and query user to select which concrete recipe to return.
        """
        await send_message(context, "Please select a recipe you would like to craft:")
        recipe_dict = {item['name']: item for item in data}
        next_key = await query_user(cog, context, recipe_dict)
        return recipe_dict[next_key]
    else:
        raise RuntimeError(f'query_until_recipe encountered bad type. label={label}; type={type};')


async def recipe_confirm(cog, context, recipe):
    message = "Would you like to craft this recipe? [Yes/No]"
    await send_message(context, "\n".join([str(recipe), message]))
    question_dict = {'yes': True, 'no': False}
    response = await get_reply(cog, context, question_dict)
    return question_dict[response]


async def ask_user_to_select_recipe(cog, context, data: dict, label):
    recipe_dict = await query_until_recipe(cog, context, data, label)
    return create_recipe(recipe_dict)

available_prereq = ['has_class', 'has_item', 'has_feat', 'has_skill', 'has_skill_proficiency',
                    'has_item_quantity_by_keyword', 'has_subclass', 'has_either_class']


async def verify_prerequisites(context, character, recipe) -> bool:
    if recipe.prereq is not None:
        for method_name, arg in recipe.prereq.items():
            method = getattr(character, method_name) if method_name in available_prereq else None
            if method is None:
                raise AttributeError(f"Invalid prereq method {method_name} for {str(recipe)}")
            else:

                if isinstance(arg, list):
                    result = method(*arg)
                elif isinstance(arg, dict):
                    result = method(**arg)
                else:
                    result = method(arg)

                if not result:
                    await send_message(context, f"Prereq {method_name}: {arg} **failed**.")
                    return False
    return True





import yaml
from Crafting.RecipeFactory import create_recipe


class StopException(Exception):
    pass


class ExitException(Exception):
    pass


def is_stop_response(response):
    if response.lower() == 'stop':
        raise StopException()


def is_exit_response(response):
    if response.lower() == 'exit':
        raise ExitException()


def is_stop_or_exit(response):
    is_stop_response(response)
    is_exit_response(response)
    return False


def get_crafting_filename():
    return "/media/sf_shared/crafting.yml"


def parse_crafting_file():
    with open(get_crafting_filename(), 'r') as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)


def send_message(context, message):
    # await context.message.author.send("No options available")
    print(message)


responses = ["1", "1", "2"]


def wait_for_reply(cog, context, question_dict):
    # check_reply = lambda r: r.author == context.author and r.channel.type[1] == 1
    # try:
    #     msg = await cog.bot.wait_for('message', timeout=120.0, check=check_reply)
    # except asyncio.TimeoutError:
    #     return "exit"
    response = ""
    while True:
        response = responses.pop(0)
        if (response in question_dict) or is_stop_or_exit(response):
            break
        else:
            message = "'{}' is invalid. Must be one of: [1..{}], 'stop', or 'exit'".format(response, len(question_dict))
            send_message(context, message)
    return response


def create_question_dict(data: dict):
    return {str(i): key for i, key in enumerate(data.keys(), start=1)}


def query_until_recipe_list(cog, context, data):
    if isinstance(data, dict):
        send_message(context, "Select a category:")
        question_dict = create_question_dict(data)
        send_message(context, "\n".join("{} : {}".format(k, v) for k, v in question_dict.items()))
        response = wait_for_reply(cog, context, question_dict)
        category = question_dict[response]
        send_message(context, "You have selected **{}**... Fetching sub-categories...".format(category))
        next_dict = data[category]
        return query_until_recipe_list(cog, context, next_dict)
    else:
        return data


def ask_user_to_select_recipe(cog, context, data: dict):
    recipe_list = query_until_recipe_list(cog, context, data)
    send_message(context, "Select a recipe:")
    question_dict = {str(i): item['name'] for i, item in enumerate(recipe_list, start=1)}
    send_message(context, "\n".join("{} : {}".format(k, v) for k, v in question_dict.items()))
    response = wait_for_reply(cog, context, question_dict)
    send_message(context, "Recipe chosen: **{}**...".format(question_dict[response]))
    return create_recipe(recipe_list[int(response)-1])


def craft_item(cog, context, character):
    data = parse_crafting_file()
    recipe = ask_user_to_select_recipe(cog, context, data)
    if recipe.can_afford(character):
        item_crafted = recipe.craft(character)
        if item_crafted is not None:
            send_message(context, "You successfully crafted **{}**".format(item_crafted))
    return

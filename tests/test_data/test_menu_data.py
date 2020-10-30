import logging
import textwrap
from typing import List
import uuid

import discord

from Character.CharacterInfoFacade import interface as character_info_interface
from Character.SkillInfoFacade import interface as skill_info_interface
from Character.Data.CharacterInfo import CharacterInfo
from Character.Character import Character

log = logging.getLogger(__name__)

help_msg = textwrap.dedent('''\
            ```
            Prospects of Thystra Bot
    
            Menu:
              menu Opens the main menu
            \u200bNo Category:
              help Shows this message
    
            Type .help command for more info on a command.
            You can also type .help category for more info on a category.
            ```''')

no_character_message = "You do not have a character which can access the menu. " \
                       "You will need to roll your stats and talk with a Mod to create your character. " \
                       "The 'randchar' command will randomly roll your characters stats. " \
                       "Once this is done, a Mod can use the 'Create' command to create your character."

discord_info_lookup = {
    'player': dict(username="TestPlayer", discrim="0001", id_num=123456789012345678),
    'non_player': dict(username="TestUser", discrim="0002", id_num=876543210987654321),
    'admin': dict(username="TestAdmin", discrim="0003", id_num=100000000000000000)
}

character_info_lookup = {
    'player': dict(character_id=uuid.UUID(int=1), roll_id=uuid.UUID(int=1),
                   discord_id=discord_info_lookup['player']['id_num'],
                   name='player', race='TestRace', background='TestBg',
                   xp=900, gold=10.0, str=20, dex=20, con=20, int=20, wis=20, cha=20
                   )
}

character_skill_lookup = {
    # 'player': [('Weaver', True)]
}

character_item_lookup = {
    'player': [('Weavers Tools', 1)]
}


def create_characters():
    for name, info in character_info_lookup.items():
        if not character_info_interface.fetch_by_discord_id(info['discord_id']):

            # Insert character info into database
            character_info_interface.insert(CharacterInfo(**info))

            # Create a Character object from database
            character: Character = Character(info['character_id'])

            # Add any applicable skills to the Character
            if name in character_skill_lookup:
                for skill_name, proficiency in character_skill_lookup[name]:
                    character.learn_skill(skill_info_interface.fetch(skill_name), proficiency)

            # Add any applicable items to the Character
            if name in character_item_lookup:
                for item_name, amount in character_item_lookup[name]:
                    character.set_item_amount(item_name, amount)


def get_base_embed_dict(title: str, description: str, fields: List[dict], color=13632027):
    return {
        'thumbnail': {
            'url': 'https://cdn3.iconfinder.com/data/icons/'
                   'fantasy-and-role-play-game-adventure-quest/512/Helmet.jpg-512.png'
        },
        'fields': fields,
        'color': color,
        'type': 'rich',
        'description': description,
        'title': title
    }

def get_main_menu_embed(player):
    title = 'Main Menu'
    description = f'Welcome, **{player}**. What can the Forgemaster do for you?'
    fields = [
                {'inline': False, 'name': 'Navigation Guide',
                 'value': "I will provide you a list of available options. "
                          "Please select an option you'd like me to perform by inputting the identifier (before `:`). "
                          "**Note:** You may select one of the listed alternate options at anytime."},
                {'inline': False, 'name': 'Please select one of the following options:',
                 'value': '**1** : Character Sheet\n**2** : Workshop\n**3** : Market\n'
                          '**stop** : Return to previous menu\n**exit** : Close this menu'}
             ]
    return discord.Embed.from_dict(get_base_embed_dict(title, description, fields))


def get_character_sheet_embed(name, level=False, pick_subclass=False, view=False, learn=False, forget=False,
                              free_profession=False, skills: List[str] = None, items: List[str] = None):
    title = 'Character Sheet'
    description = f'**{name}**, welcome to your character sheet. ' \
                  f'This menu displays a summary of info for your character and allows you to manage your character.'
    end_options = '**stop** : Return to previous menu\n**exit** : Close this menu'
    possible_options = [
        (level, 'Level up your character'),
        (pick_subclass, 'Pick available subclass'),
        (view, 'View your spells'),
        (learn, 'Learn a spell'),
        (forget, 'Forget a spell'),
        (free_profession, 'Pick a free profession')
    ]
    valid_options = [label for valid, label in possible_options if valid]

    # Create options for player
    options_string = "\n".join(f"**{i}** : {option}" for i, option in enumerate(valid_options, start=1))
    options_string = "\n".join([options_string, end_options])

    item_string = None
    if items:
        skill_string = ", ".join(f"{item}" for item in items)
    elif name in character_item_lookup:
        items = character_item_lookup[name]
        item_string = ", ".join(f"{amount}x[{item_name}]" for item_name, amount in items)
    item_string = item_string if item_string else "None"

    skill_string = None
    if skills:
        skill_string = ", ".join(f"{skill}" for skill in skills)
    elif name in character_skill_lookup:
        skills = character_skill_lookup[name]
        skill_string = ", ".join(f"{skill}{'' if proficiency else ' (D)'}" for skill, proficiency in skills)
    skill_string = skill_string if skill_string else "None"


    # Create fields and return the embed
    fields = [
                {'inline': True, 'name': 'Name', 'value': f"{name}"},
                {'inline': True, 'name': 'XP', 'value': f"{character_info_lookup[name]['xp']}"},
                {'inline': True, 'name': 'Gold', 'value': f"{character_info_lookup[name]['gold']}"},
                {'inline': True, 'name': 'Feats', 'value': 'None'},
                {'inline': True, 'name': 'Skills', 'value': skill_string},
                {'inline': False, 'name': 'Stats', 'value': 'STR: 20, DEX: 20, CON: 20, INT: 20, WIS: 20, CHA: 20'},
                {'inline': True, 'name': 'Items', 'value': item_string},
                {'inline': False, 'name': 'Please select one of the following options:',
                 'value': options_string}
            ]
    return discord.Embed.from_dict(get_base_embed_dict(title, description, fields))


help_text = textwrap.dedent('''\
            ```
            This is a test bot for text menus.
            
            \u200bNo Category:
              help Shows this message
            
            Type .help command for more info on a command.
            You can also type .help category for more info on a category.
            ```''')

import Crafting.Parser
import Crafting.RecipeFactory
import yaml

resistance_data = {'Resistances': ['Acid Resistance', 'Cold Resistance', 'Fire Resistance', 'Force Resistance', 'Lightning Resistance',
                                   'Necrotic Resistance', 'Poison Resistance', 'Psychic Resistance', 'Radiant Resistance', 'Thunder Resistance']}


def replace_str_in_variants(name, variant_items, to_find):
    return [name.replace(to_find, item) for item in variant_items]


def replace_armor(name, variant_items):
    if isinstance(variant_items, str):
        variant_items = [variant_items]
    return replace_str_in_variants(name, variant_items, 'Armor')


def replace_sword(name, variant_items):
    if isinstance(variant_items, str):
        variant_items = [variant_items]
    return replace_str_in_variants(name, variant_items, 'Sword')


def replace_weapon(name, variant_items):
    if isinstance(variant_items, str):
        variant_items = [variant_items]
    return replace_str_in_variants(name, variant_items, 'Weapon')


def replace_blade(name, variant_items):
    if isinstance(variant_items, str):
        variant_items = [variant_items]
    return replace_str_in_variants(name, variant_items, 'Blade')


def replace_axe(name, variant_items):
    if isinstance(variant_items, str):
        variant_items = [variant_items]
    return replace_str_in_variants(name, variant_items, 'Axe')


def replace_resistance(name, variant_items):
    if isinstance(variant_items, str):
        variant_items = [variant_items]
    return replace_str_in_variants(name, resistance_data['Resistances'], '<Resistance>')


replacement_data = {'Armor': replace_armor,
                    '<Resistance>': replace_resistance,
                    'Sword': replace_sword,
                    'Weapon': replace_weapon,
                    'Blade': replace_blade,
                    'Axe': replace_axe
                    }


def parse_slot_data(data):
    slot_items = []
    if isinstance(data, dict):
        if len(data.keys()) == 1:
            name, variants = list(data.items())[0]
            print(f"Parsing variant items for {name}")

            replacement_steps = [v for k, v in replacement_data.items() if k in name]
            variant_items = []
            if not replacement_steps:
                for variant in flatten(variants):
                    variant_items.append(f"{name} - {variant}")
            else:
                for step in replacement_steps:
                    # print(f"Before step: {variant_items}")
                    new_variants = []
                    if not variant_items:
                        new_variants.extend(step(name, flatten(variants)))
                    else:
                        for item in variant_items:
                            new_variants.extend(step(item, variant_items))
                    variant_items = new_variants
                    # print(f"After step: {variant_items}")
            slot_items.extend(variant_items)
    else:
        if '<Resistance>' in data:
            data = replacement_data['<Resistance>'](data, data)
        slot_items.append(data)
    return slot_items


item_data = Crafting.Parser.parse_file("RedThaumstynApprovedMagicItems.latest")['Items']
recipes = {}
for rarity, rarity_data in item_data.items():
    recipes[rarity] = {}
    for slot, slot_data in rarity_data.items():
        items = []
        for item in slot_data:
            items.extend(Crafting.RecipeFactory.parse_slot_data(item))
    recipes[rarity][slot] = items
print(recipes)
with open('parsed.yaml', 'w') as yaml_file:
    yaml.dump(recipes, yaml_file, default_flow_style=False)


strings = []
depth = 0
spacing = "  "
with open('/media/sf_shared/parsed.yaml') as stream:
    magic_items = yaml.load(stream, Loader=yaml.FullLoader)
strings.append(f"{spacing*depth}Magic Item:")
depth = depth + 1
rarity_depth = depth
for rarity_key in magic_items.keys():
    depth = rarity_depth
    strings.append(f"{spacing*depth}{rarity_key}:")
    rarity_data = magic_items[rarity_key]
    depth = depth+1
    slot_depth = depth
    for slot_key in rarity_data.keys():
        slot_data = rarity_data[slot_key]
        depth = slot_depth
        strings.append(f"{spacing*depth}{slot_key}:")
        depth = depth+1
        item_depth = depth
        for item in slot_data:
            depth = item_depth
            strings.append(f"{spacing*depth}-")
            depth = depth+1
            strings.append(f"{spacing * depth}name: {item}")
            #strings.append(f"{spacing * depth}cost:")
            #strings.append(f"{spacing * depth}{spacing}Red Dust: 100")
            #strings.append(f"{spacing * depth}special:")
            #strings.append(f"{spacing * depth}{spacing}random outcome:")
            #strings.append(f"{spacing * depth}{spacing}{spacing}<<: *Special_Magic_Item_{rarity_key}_{slot_key}_Random_Outcome")
            strings.append(f"{spacing * depth}<<: *Recipe_Magic_Item_{rarity_key.replace(' ','_')}_{slot_key.replace(' ','_')}_Rules")
            strings.append(f"{spacing * depth}outcomes:")
            strings.append(f"{spacing * depth}{spacing}- {item}")
with open('test.yaml', 'w') as f:
    f.writelines(f"{line}\n" for line in strings)

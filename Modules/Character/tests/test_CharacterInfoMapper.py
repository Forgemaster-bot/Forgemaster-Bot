#!/usr/bin/env python3
import unittest
from Quick_Python import run_query_commit
import Character.CharacterInfoFacade
import Character.Data.CharacterInfo
import Connections


def delete_table_rows(table: str):
    query = """\
        DELETE FROM [{table}]
        """.format(table=table)
    run_query_commit(query)


character_id = '0E984725-C51C-4BF4-9960-E1C80E27ABA0'
discord_id = "1234"
name = 'test_name'
race = 'test_race'
background = 'test_background'
xp = 0
strength = 1
dex = 2
con = 3
intelligence = 4
wis = 5
cha = 6
gold = 7
roll_id = '8616E10E-0D7C-457C-8C89-E661A45264FB'
roll_id_binary = b'\x0e\xe1\x16\x86|\r|E\x8c\x89\xe6a\xa4Rd\xfb'


def insert_character():
    query = """\
    insert into Main_Characters 
    (ID,Discord_ID,Character_Name,Race,Background,XP,Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,Roll_ID) 
    values 
    (CONVERT(uniqueidentifier,?),?,?,?,?,?,?,?,?,?,?,?,?,CONVERT(uniqueidentifier,?))
    """
    cursor = run_query_commit(query,
                              [character_id, discord_id, name, race, background, xp, strength, dex, con, intelligence,
                               wis, cha, gold, roll_id])


class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        delete_table_rows("Main_Characters")
        insert_character()

    @classmethod
    def tearDownClass(cls):
        delete_table_rows("Main_Characters")

    def test_initializer_empty(self):
        character = Character.Data.CharacterInfo.CharacterInfo()
        self.assertEqual(character.name, None)

    def test_initializer_valid(self):
        character = Character.Data.CharacterInfo.CharacterInfo(name=name)
        self.assertEqual(character.name, name)

    def test_initializer_invalid(self):
        with self.assertRaises(AttributeError):
            character = Character.Data.CharacterInfo.CharacterInfo(**{'not_real_attr': None})

    def test_fetch_info(self):
        character_list = Character.CharacterInfoFacade.interface.fetch(character_id)
        self.assertEqual(len(character_list), 1)
        character = character_list[0]
        # Assert each field
        self.assertEqual(character.discord_id, discord_id)
        self.assertEqual(character.name, name)
        self.assertEqual(character.race, race)
        self.assertEqual(character.background, background)
        self.assertEqual(character.str, strength)
        self.assertEqual(character.dex, dex)
        self.assertEqual(character.con, con)
        self.assertEqual(character.int, intelligence)
        self.assertEqual(character.wis, wis)
        self.assertEqual(character.cha, cha)
        self.assertEqual(character.gold, gold)
        self.assertEqual(character.roll_id, roll_id_binary)

    def test_insert(self):
        discid = discord_id+'1'
        start_size = len(Character.CharacterInfoFacade.interface.fetch_by_discord_id(discid))
        self.assertEqual(start_size, 0)
        character = Character.Data.CharacterInfo.CharacterInfo(discord_id=discid,
                                                               name=name,
                                                               race=race,
                                                               background=background,
                                                               str=strength,
                                                               dex=dex,
                                                               con=con,
                                                               int=intelligence,
                                                               wis=wis,
                                                               cha=cha,
                                                               gold=gold,
                                                               xp=xp,
                                                               roll_id=roll_id)
        print(character.to_dict())
        Character.CharacterInfoFacade.interface.insert(character)
        characters = Character.CharacterInfoFacade.interface.fetch_by_discord_id(discid)
        end_size = len(characters)
        self.assertEqual(start_size + 1, end_size)
        inserted_character = characters[end_size-1]
        # Assert each field
        self.assertEqual(character.discord_id, inserted_character.discord_id)
        self.assertEqual(character.name, inserted_character.name)
        self.assertEqual(character.race, inserted_character.race)
        self.assertEqual(character.background, inserted_character.background)
        self.assertEqual(character.str, inserted_character.str)
        self.assertEqual(character.dex, inserted_character.dex)
        self.assertEqual(character.con, inserted_character.con)
        self.assertEqual(character.int, inserted_character.int)
        self.assertEqual(character.wis, inserted_character.wis)
        self.assertEqual(character.cha, inserted_character.cha)
        self.assertEqual(character.gold, inserted_character.gold)
        self.assertEqual(roll_id_binary, inserted_character.roll_id)


if __name__ == '__main__':
    unittest.main()

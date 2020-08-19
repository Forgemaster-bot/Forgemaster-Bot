import unittest
from Quick_Python import run_query_commit
from Character import CharacterClassFacade
from Character.Data.CharacterID import CharacterID
from Character.Data.CharacterClass import CharacterClass

test_data = {'character_id': '0E984725-C51C-4BF4-9960-E1C80E27ABA0',
             'class_name': 'Test',
             'level': 1,
             'number': 1,
             'subclass': None,
             'free_book_spells': 0,
             'can_replace_spells': 1,
             'has_class_choice': 1}


def delete_table_rows(table: str):
    query = """\
        DELETE FROM [{table}]
        """.format(table=table)
    run_query_commit(query)


class InitializerTestCase(unittest.TestCase):
    def test_initializer_empty(self):
        character_class = CharacterClass()
        self.assertEqual(character_class.character_id, None)

    def test_initializer_valid_kw(self):
        character_class = CharacterClass(character_id='test')
        self.assertEqual(character_class.character_id, 'test')

    def test_initializer_valid_dict(self):
        character_class = CharacterClass(**test_data)
        for k, v in test_data.items():
            self.assertEqual(getattr(character_class, k), v)

    def test_initializer_invalid(self):
        with self.assertRaises(AttributeError):
            CharacterClass(**{'not_real_attr': None})


class MapperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        delete_table_rows(CharacterClassFacade.interface._mapper._table_info.table)

    @classmethod
    def tearDownClass(cls):
        delete_table_rows(CharacterClassFacade.interface._mapper._table_info.table)

    def test_insert_and_fetch(self):
        character_id = test_data['character_id']
        start_size = len(CharacterClassFacade.interface.fetch(character_id))
        self.assertEqual(start_size, 0)

        CharacterClassFacade.interface.insert(CharacterClass(**test_data))
        character_classes = CharacterClassFacade.interface.fetch(character_id)
        self.assertEqual(start_size + 1, len(character_classes))

        for character_class in character_classes:
            test_item = test_data.pop('character_id')
            for k, v in test_data.items():
                self.assertEqual(getattr(character_class, k), v)


if __name__ == '__main__':
    unittest.main()

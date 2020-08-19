import unittest
from Quick_Python import run_query_commit
from Character import CharacterFeatFacade as Facade
from Character.Data.CharacterFeat import CharacterFeat as DataClass

test_data = {'character_id': '0E984725-C51C-4BF4-9960-E1C80E27ABA0',
             'name': 'ASI'}


def delete_table_rows(table: str):
    query = """\
        DELETE FROM [{table}]
        """.format(table=table)
    run_query_commit(query)


class InitializerTestCase(unittest.TestCase):
    def test_initializer_empty(self):
        character_class = DataClass()
        self.assertEqual(character_class.character_id, None)

    def test_initializer_valid_kw(self):
        character_class = DataClass(character_id='test')
        self.assertEqual(character_class.character_id, 'test')

    def test_initializer_valid_dict(self):
        character_class = DataClass(**test_data)
        for k, v in test_data.items():
            self.assertEqual(getattr(character_class, k), v)

    def test_initializer_invalid(self):
        with self.assertRaises(AttributeError):
            DataClass(**{'not_real_attr': None})


class MapperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        delete_table_rows(Facade.interface._mapper._table_info.table)

    @classmethod
    def tearDownClass(cls):
        delete_table_rows(Facade.interface._mapper._table_info.table)

    def test_insert_and_fetch(self):
        character_id = test_data['character_id']
        start_size = len(Facade.interface.fetch(character_id))
        self.assertEqual(start_size, 0)

        Facade.interface.insert(DataClass(**test_data))
        character_classes = Facade.interface.fetch(character_id)
        self.assertEqual(start_size + 1, len(character_classes))

        for character_class in character_classes:
            test_item = test_data.pop('character_id')
            for k, v in test_data.items():
                self.assertEqual(getattr(character_class, k), v)


if __name__ == '__main__':
    unittest.main()

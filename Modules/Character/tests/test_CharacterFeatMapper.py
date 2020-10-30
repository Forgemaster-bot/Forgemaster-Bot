import unittest
from Quick_Python import run_query_commit
from Character import CharacterFeatFacade as Facade
from Character.Data.CharacterFeat import CharacterFeat as DataClass

test_data = {'character_id': '0E984725-C51C-4BF4-9960-E1C80E27ABA0',
             'name': 'ASI'}
test_update_field = 'name'


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
        objects = Facade.interface.fetch(character_id)
        self.assertEqual(len(objects), 1)
        test_item = objects[0]

        data = test_data
        data.pop('character_id')
        for k, v in data.items():
            self.assertEqual(getattr(test_item, k), v)

        # Update the item
        old_value = getattr(test_item, test_update_field)
        new_value = getattr(test_item, test_update_field)*2
        setattr(test_item, test_update_field, new_value)
        with self.assertRaises(RuntimeError):
            Facade.interface.update(test_item)
        setattr(test_item, test_update_field, old_value)

        # Remove the item
        Facade.interface.delete(test_item)

        # Test the remove was successful
        objects = Facade.interface.fetch(character_id)
        self.assertEqual(len(objects), 0)

if __name__ == '__main__':
    unittest.main()

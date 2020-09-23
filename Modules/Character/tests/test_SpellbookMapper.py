import unittest
from Quick_Python import run_query_commit
from Character import SpellbookFacade as Facade
from Character.Data.Spellbook import Spellbook as DataClass

test_character_id = '0E984725-C51C-4BF4-9960-E1C80E27ABA0'
test_data = {'spellbook_id': 'F76D5725-E157-4B7E-8945-AC2AFA7C8876',
             'character_id': test_character_id,
             'name': 'Guin Spellbook',
             'type': 'Core'}

binary_id = b'%Wm\xf7W\xe1~K\x89E\xac*\xfa|\x88v'

test_update_field = 'type'

def delete_table_rows(table: str, column=None, value=None):
    if column is None or value is None:
        query = f"DELETE FROM [{table}]"
        args = None
    else:
        query = f"DELETE FROM [{table}] WHERE [{column}] = ?"
        args = [value]
    run_query_commit(query, args)


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
        with self.assertRaises(TypeError):
            DataClass(**{'not_real_attr': None})


class MapperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        delete_table_rows(Facade.interface._mapper._table_info.table,
                          Facade.interface._mapper._table_info.character_id,
                          test_character_id)

    @classmethod
    def tearDownClass(cls):
        pass
        delete_table_rows(Facade.interface._mapper._table_info.table,
                          Facade.interface._mapper._table_info.character_id,
                          test_character_id)

    def test_insert_and_fetch(self):
        character_id = test_data['character_id']
        id = test_data['spellbook_id']

        start_size = len(Facade.interface.fetch(character_id))
        self.assertEqual(start_size, 0)

        Facade.interface.insert(DataClass(**test_data))
        objects = Facade.interface.fetch_by_character_id(character_id)
        self.assertEqual(len(objects), 1)
        test_item = objects[0]

        data = test_data
        data.pop('character_id')
        data.pop('spellbook_id')
        for k, v in data.items():
            self.assertEqual(getattr(test_item, k), v)

        # Update the item
        new_value = getattr(test_item, test_update_field)*2
        setattr(test_item, test_update_field, new_value)
        Facade.interface.update(test_item)

        # Test the update was successful
        objects = Facade.interface.fetch(id)
        self.assertEqual(len(objects), 1)
        test_item = objects[0]
        self.assertEqual(getattr(test_item, test_update_field), new_value)

        # Remove the item
        Facade.interface.delete(test_item)

        # Test the remove was successful
        objects = Facade.interface.fetch(character_id)
        self.assertEqual(len(objects), 0)


if __name__ == '__main__':
    unittest.main()

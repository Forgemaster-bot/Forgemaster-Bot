import unittest
from Quick_Python import run_query_commit
from Character import SpellbookSpellFacade as Facade
from Character.Data.SpellbookSpell import SpellbookSpell as DataClass

test_spellbook_id = '5E984725-C51C-4BF4-9960-E1C80E27ABA0'
test_data = {'spellbook_id': test_spellbook_id,
             'name': 'Spell#1',
             'is_known': True}

binary_id = b'%Wm\xf7W\xe1~K\x89E\xac*\xfa|\x88v'

test_update_field = 'is_known'

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
        self.assertEqual(character_class.spellbook_id, None)

    def test_initializer_valid_kw(self):
        character_class = DataClass(spellbook_id='test')
        self.assertEqual(character_class.spellbook_id, 'test')

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
        delete_table_rows(Facade.interface._mapper._table_info.table,
                          Facade.interface._mapper._table_info.spellbook_id,
                          test_spellbook_id)

    @classmethod
    def tearDownClass(cls):
        pass
        delete_table_rows(Facade.interface._mapper._table_info.table,
                          Facade.interface._mapper._table_info.spellbook_id,
                          test_spellbook_id)

    def test_insert_and_fetch(self):
        spellbook_id = test_data['spellbook_id']

        start_size = len(Facade.interface.fetch(spellbook_id))
        self.assertEqual(start_size, 0)

        Facade.interface.insert(DataClass(**test_data))
        objects = Facade.interface.fetch(spellbook_id)
        self.assertEqual(len(objects), 1)
        test_item = objects[0]

        data = test_data
        data.pop('spellbook_id')
        for k, v in data.items():
            self.assertEqual(getattr(test_item, k), v)

        # Update the item
        new_value = not getattr(test_item, test_update_field)
        setattr(test_item, test_update_field, new_value)
        Facade.interface.update(test_item)

        # Test the update was successful
        objects = Facade.interface.fetch(spellbook_id)
        self.assertEqual(len(objects), 1)
        test_item = objects[0]
        self.assertEqual(getattr(test_item, test_update_field), new_value)

        # Remove the item
        Facade.interface.delete(test_item)

        # Test the remove was successful
        objects = Facade.interface.fetch(spellbook_id)
        self.assertEqual(len(objects), 0)


if __name__ == '__main__':
    unittest.main()

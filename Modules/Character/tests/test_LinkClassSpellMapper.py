import unittest
from Character import LinkClassSpellFacade as Facade
from Character.Data.LinkClassSpell import LinkClassSpell as DataClass

test_data = {"class_name": "Cleric",
             "spell_name": "Protection from Good and Evil"}

spell_level = 1

class InitializerTestCase(unittest.TestCase):
    def test_initializer_empty(self):
        with self.assertRaises(RuntimeError):
            character_class = DataClass()

    def test_initializer_valid_kw(self):
        with self.assertRaises(RuntimeError):
            character_class = DataClass(class_name='test')

    def test_initializer_valid_dict(self):
        character_class = DataClass(**test_data)
        for k, v in test_data.items():
            self.assertEqual(getattr(character_class, k), v)

    def test_initializer_invalid(self):
        with self.assertRaises(TypeError):
            DataClass(**{'not_real_attr': None})


class MapperTestCase(unittest.TestCase):

    def test_insert_and_fetch(self):
        name = test_data['class_name']

        test_items = Facade.interface.fetch(name)
        self.assertEqual(10, len(test_items))

        level_1_spells = test_items[1]
        self.assertEqual(16, len(level_1_spells))

        test_item = level_1_spells[test_data['spell_name']]
        data = test_data
        for k, v in data.items():
            self.assertEqual(getattr(test_item, k), v)

        test_item = Facade.interface.fetch("does not exist")
        self.assertEqual(test_item, None)


if __name__ == '__main__':
    unittest.main()

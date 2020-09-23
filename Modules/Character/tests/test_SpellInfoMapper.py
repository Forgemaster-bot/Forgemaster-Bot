import unittest
from Character import SpellInfoFacade as Facade
from Character.Data.SpellInfo import SpellInfo as DataClass

test_data = {"name": "Absorb Elements",
             "level": 1,
             "school": "Abjuration",
             "ritual": False,
             "source": "Elemental Evil",
             "consumable_cost": 0}

class InitializerTestCase(unittest.TestCase):
    def test_initializer_empty(self):
        character_class = DataClass()
        self.assertEqual(character_class.name, None)

    def test_initializer_valid_kw(self):
        character_class = DataClass(name='test')
        self.assertEqual(character_class.name, 'test')

    def test_initializer_valid_dict(self):
        character_class = DataClass(**test_data)
        for k, v in test_data.items():
            self.assertEqual(getattr(character_class, k), v)

    def test_initializer_invalid(self):
        with self.assertRaises(TypeError):
            DataClass(**{'not_real_attr': None})


class MapperTestCase(unittest.TestCase):

    def test_insert_and_fetch(self):
        name = test_data['name']

        test_item = Facade.interface.fetch(name)
        self.assertTrue(test_item is not None)

        data = test_data
        for k, v in data.items():
            self.assertEqual(getattr(test_item, k), v)

        test_item = Facade.interface.fetch("does not exist")
        self.assertIsNone(test_item)


if __name__ == '__main__':
    unittest.main()

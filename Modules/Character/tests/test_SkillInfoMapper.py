import unittest
from Character import SkillInfoFacade as Facade
from Character.Data.SkillInfo import SkillInfo as DataClass

test_data = {"name": "Herbalist",
             "ability": "Intelligence",
             "is_job": True,
             "tool": "Herbalism Kit",
             "consumable_name": "Potion"
}

class InitializerTestCase(unittest.TestCase):
    def test_initializer_empty(self):
        obj = DataClass()
        self.assertEqual(obj.name, None)

    def test_initializer_valid_kw(self):
        obj = DataClass(name='test')
        self.assertEqual(obj.name, 'test')

    def test_initializer_valid_dict(self):
        obj = DataClass(**test_data)
        for k, v in test_data.items():
            self.assertEqual(getattr(obj, k), v)

    def test_initializer_invalid(self):
        with self.assertRaises(TypeError):
            DataClass(**{'not_real_attr': None})


class MapperTestCase(unittest.TestCase):

    def test_insert_and_fetch(self):
        name = test_data['name']

        # Case one, unknown item
        test_item = Facade.interface.fetch("does not exist")
        self.assertIsNone(test_item)

        # Case two, known item
        test_item = Facade.interface.fetch(name)
        self.assertTrue(test_item is not None)

        # Assert fields of known item
        data = test_data
        for k, v in data.items():
            self.assertEqual(getattr(test_item, k), v)

        # Special case 1, fetch all
        test_dict = Facade.interface.fetch_all()
        self.assertTrue(len(test_dict) > 0)

        # Special case 2, fetch jobs
        test_dict = Facade.interface.fetch_jobs()
        self.assertTrue(len(test_dict) > 0)
        self.assertTrue(test_item.name in test_dict)


if __name__ == '__main__':
    unittest.main()

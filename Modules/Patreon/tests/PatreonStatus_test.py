import unittest
from Quick_Python import run_query_commit

from Patreon.PatreonStatus import PatreonStatus


def delete_table_rows(table: str):
    query = """\
        DELETE FROM [{table}]
        """.format(table=table)
    run_query_commit(query)


def insert_info_discord_row(identifier: str, num_characters: int, is_patreon: bool):
    query = """\
        INSERT INTO Info_Discord (ID,Name,Character_Number,Patreon) VALUES (?,?,?,?)
        """
    args = [identifier, identifier, num_characters, is_patreon]
    run_query_commit(query, args)


class Case:
    def __init__(self, identifier, num_characters, is_patreon: bool):
        self.identifier = identifier
        self.num_characters = num_characters
        self.is_patreon = is_patreon
        insert_info_discord_row(identifier, num_characters, is_patreon)

    def select(self):
        return PatreonStatus.select(self.identifier)

    def toggle(self):
        self.is_patreon = not self.is_patreon
        PatreonStatus.set(self.identifier, self.is_patreon)


class TestPatreonStatus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        delete_table_rows("Info_Discord")

    def run_case(self, identifier, num_characters, is_patreon: bool):
        case = Case(identifier, num_characters, is_patreon)
        # Assert select works
        self.assertEqual(is_patreon, case.select())
        # Toggle value in case and then assert set works by checking new value
        case.toggle()
        self.assertNotEqual(is_patreon, case.select())

    def test_patreon_true(self):
        self.run_case("not_patreon", 0, False)

    def test_patreon_false(self):
        self.run_case("is_patreon", 0, True)

    def test_patreon_above_true(self):
        case = Case("is_patreon-above_one", 0, 2)
        self.assertTrue(case.select())

    def test_select_unknown_id(self):
        self.assertIsNone(PatreonStatus.select("not_valid_user"))

    def test_set_unknown_id(self):
        PatreonStatus.update("not_valid_user", False)
        self.assertIsNone(PatreonStatus.select("not_valid_user"))


if __name__ == '__main__':
    unittest.main()

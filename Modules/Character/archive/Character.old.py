from Character.Info import Info
from Character.Data.CharacterID import CharacterID


class Character:
    character_id = None
    info = None

    def __init__(self, character_id: CharacterID):
        """
        Initializer based on a character_id
        :param character_id: character_id used to fetch other info
        """
        if character_id is None:
            raise ValueError("Character cannot be initialized with character_id of 'None'")
        self.character_id = character_id

    def fetch_info(self):
        """
        Initializes info member object
        :return: self
        """
        self.info = Info().fetch(self.character_id)
        return self

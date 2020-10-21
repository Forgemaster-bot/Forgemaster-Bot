from Character.SpellInfoFacade import interface as spell_info_interface
class CharacterSpell:
    __slots__ = ["character_id", "name", "origin", "spell_info"]

    def __init__(self, character_id=None, name=None, origin=None):
        self.character_id = character_id
        self.name = name
        self.origin = origin
        self.spell_info = spell_info_interface.fetch(self.name)

    def to_dict(self) -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Name**
            - value = Attribute **Value**
        :return: [dict] dictionary of enumerated fields
        """
        return {s: getattr(self, s, None) for s in self.__slots__}

    def __str__(self):
        return f"{self.name}"



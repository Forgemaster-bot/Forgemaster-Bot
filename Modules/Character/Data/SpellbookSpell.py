from Character.SpellInfoFacade import interface as spell_info_interface
class SpellbookSpell:
    __slots__ = ["spellbook_id", "name", "is_known", "spell_info"]

    def __init__(self, spellbook_id=None, name=None, is_known=False):
        self.spellbook_id = spellbook_id
        self.name = name
        self.is_known = is_known
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



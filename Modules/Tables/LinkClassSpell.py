from Character.SpellInfoFacade import interface as spell_info_interface


class LinkClassSpell:
    __slots__ = ["class_name", "spell_name", "spell_info"]

    def __init__(self, class_name=None, spell_name=None):
        self.class_name = class_name
        self.spell_name = spell_name
        self.spell_info = spell_info_interface.fetch(self.spell_name)
        if self.spell_info is None:
            raise RuntimeError(f"{self.spell_name} does not exist in spell info")

    def to_dict(self) -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Name**
            - value = Attribute **Value**
        :return: [dict] dictionary of enumerated fields
        """
        return {s: getattr(self, s, None) for s in self.__slots__}

    def __str__(self):
        return f"{self.class_name} - {self.spell_name}"

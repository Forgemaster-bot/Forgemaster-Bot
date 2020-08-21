class CharacterClass:
    __slots__ = ["character_id", "name", "level", "number", "subclass",
                 "free_book_spells", "can_replace_spells", "has_class_choice"]

    def __init__(self, **kwargs):
        self.character_id = None
        self.name = None
        self.level = None
        self.number = None
        self.subclass = None
        self.free_book_spells = None
        self.can_replace_spells = None
        self.has_class_choice = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Name**
            - value = Attribute **Value**
        :return: [dict] dictionary of enumerated fields
        """
        return {s: getattr(self, s, None) for s in self.__slots__}

    def __str__(self):
        if self.subclass is None:
            return "{}: {}".format(self.name, self.level)
        else:
            return "{} {}: {}".format(self.name, self.subclass, self.level)

    def subclass_is_picked(self):
        return False if self.subclass is None else True

    def is_spell_caster(self):
        raise NotImplementedError("Not implemented yet")


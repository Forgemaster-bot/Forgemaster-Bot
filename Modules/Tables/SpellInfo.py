class SpellInfo:
    __slots__ = ["name", "level", "school", "ritual", "source", "consumable_cost"]

    def __init__(self, name=None, level=None, school=None, ritual=None, source=None, consumable_cost=None):
        self.name = name
        self.level = level
        self.school = school
        self.ritual = ritual
        self.source = source
        self.consumable_cost = consumable_cost

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

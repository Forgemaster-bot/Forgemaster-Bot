class CharacterItem:
    __slots__ = ["character_id", "name", "quantity"]

    def __init__(self, **kwargs):
        self.character_id = None
        self.name = None
        self.quantity = None
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
        return "**{}**x[**{}**]".format(self.quantity, self.name)

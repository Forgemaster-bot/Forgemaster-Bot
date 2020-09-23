import uuid

class CharacterSkill:
    __slots__ = ["character_id", "name", "proficiency"]

    def __init__(self, character_id: uuid.UUID = None, name: str =None, proficiency: bool = False):
        self.character_id: uuid.UUID = character_id
        self.name: str = name
        self.proficiency: bool = proficiency

    def to_dict(self) -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Name**
            - value = Attribute **Value**
        :return: [dict] dictionary of enumerated fields
        """
        return {s: getattr(self, s, None) for s in self.__slots__}

    def __str__(self):
        if self.proficiency == 1:
            return "{}".format(self.name)
        else:
            return "{} {}".format(self.name, "(D)")

class SkillInfo:
    __slots__ = ["name", "ability", "is_job", "tool", "consumable_name"]

    def __init__(self, name=None, ability=None, is_job=False, tool=None, consumable_name=None):
        self.name = name
        self.ability = ability
        self.is_job = is_job
        self.tool = tool
        self.consumable_name = consumable_name

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

class Character:
    __slots__ = ['background', 'cha', 'character_id', 'con',
                 'dex', 'discord_id', 'gold', 'int', 'name',
                 'race', 'roll_id', 'str', 'wis', 'xp']

    def __init__(self, **kwargs):
        """
        Initialize member attributes and then use keywords to set values
        :param kwargs: keyword arguments for setting member attributes
        """
        self.character_id = None
        self.discord_id = None
        self.name = None
        self.race = None
        self.background = None
        self.xp = None
        self.str = None
        self.dex = None
        self.con = None
        self.int = None
        self.wis = None
        self.cha = None
        self.gold = None
        self.roll_id = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Name**
            - value = Attribute **Value**
        :return: [dict] dictionary of enumerated fields
        """
        # return {k: v for k, v in self.__members__.items()}
        return {s: getattr(self, s, None) for s in self.__slots__}

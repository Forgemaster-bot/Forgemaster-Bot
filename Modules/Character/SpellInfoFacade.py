import Character.Tables.SpellInfoMapper as Mapper
from Character.Data.SpellInfo import SpellInfo
from typing import List

class SpellInfoFacade:
    """
    Facade for fetching and saving a character
    """
    # Define class variable to hold spells. This will start as None but be filled in on the first fetch call.
    spells = None

    def __init__(self, mapper):
        self._mapper = mapper

    def _fetch(self) -> List[SpellInfo]:
        if self.__class__.spells is None:
            spell_name_col = Mapper.mapper.table_info.name
            self.__class__.spells = {s.name: s for s in self._mapper.fetch(column=spell_name_col, value="*")}
        return self.__class__.spells

    def fetch(self, spell_name: str) -> SpellInfo:
        """
        Fetches spell info if it hasn't been fetched before.
        :param spell_name:
        :return:
        """
        spells = self._fetch()
        return spells[spell_name] if spell_name in spells else None


interface = SpellInfoFacade(Mapper.mapper)

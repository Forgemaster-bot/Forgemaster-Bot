import Character.Tables.LinkClassSpellMapper as Mapper
from Character.Data.LinkClassSpell import LinkClassSpell
from typing import Dict, List
import itertools


class LinkClassSpellFacade:
    """
    Facade for fetching and saving a character
    """
    # Define class variable to hold spells. This will start as None but be filled in on the first fetch call.
    spells = None

    def __init__(self, mapper):
        self._mapper = mapper

    def _fetch(self) -> Dict[str, Dict[int, List[LinkClassSpell]]]:
        if self.__class__.spells is None:
            self.__class__.spells = {}
            spells = self._mapper.fetch(column=Mapper.mapper.table_info.class_name, value="*")
            # Sort before using groupby
            spells = sorted(spells, key=lambda spell: (spell.class_name, spell.spell_info.level))
            for key, group in itertools.groupby(spells, lambda spell: (spell.class_name, spell.spell_info.level)):
                class_name = key[0]
                spell_level = key[1]
                if class_name not in self.__class__.spells:
                    self.__class__.spells[class_name] = {}
                self.__class__.spells[class_name][spell_level] = {spell.spell_name: spell for spell in group}
        return self.__class__.spells

    def fetch(self, class_name: str) -> Dict[int, List[LinkClassSpell]]:
        """
        Fetches spell info if it hasn't been fetched before.
        :param class_name:
        :return:
        """
        spells = self._fetch()
        return spells[class_name] if class_name in spells else None


interface = LinkClassSpellFacade(Mapper.mapper)

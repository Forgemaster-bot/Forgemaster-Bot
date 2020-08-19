import Character.Tables.CharacterSkillMapper as CharacterSkillMapper
from Character.Data.CharacterSkill import CharacterSkill
from typing import List


class CharacterSkillFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, character_id: str) -> List[CharacterSkill]:
        return self._mapper.fetch(character_id)

    def update(self, character: CharacterSkill):
        return self._mapper.update(character)

    def insert(self, character: CharacterSkill):
        return self._mapper.insert(character)


interface = CharacterSkillFacade(CharacterSkillMapper.mapper)

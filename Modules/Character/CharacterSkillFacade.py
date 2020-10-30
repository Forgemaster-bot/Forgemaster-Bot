import Character.Tables.CharacterSkillMapper as CharacterSkillMapper
from Character.Data.CharacterSkill import CharacterSkill
from typing import List


class CharacterSkillFacade:
    """
    Facade for fetching and saving a character skill
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, skill_name: str) -> List[CharacterSkill]:
        return self._mapper.fetch(skill_name)

    def update(self, skill: CharacterSkill):
        return self._mapper.update(skill)

    def insert(self, skill: CharacterSkill):
        return self._mapper.insert(skill)

    def delete(self, skill: CharacterSkill):
        return self._mapper.delete(skill)


interface = CharacterSkillFacade(CharacterSkillMapper.mapper)

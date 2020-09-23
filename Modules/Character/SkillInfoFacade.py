import Character.Tables.SkillInfoMapper as Mapper
from Character.Data.SkillInfo import SkillInfo
from typing import List
from typing import Dict

class SkillInfoFacade:
    """
    Facade for fetching and saving a character
    """
    # Define class variable to hold Skills. This will start as None but be filled in on the first fetch call.
    skills = None

    def __init__(self, mapper):
        self._mapper = mapper

    def _fetch(self) -> Dict[str, SkillInfo]:
        if self.__class__.skills is None:
            skill_name_col = Mapper.mapper.table_info.name
            self.__class__.skills = {s.name: s for s in self._mapper.fetch(column=skill_name_col, value="*")}
        return self.__class__.skills

    def fetch(self, skill_name: str) -> SkillInfo:
        """
        Fetches Skill info if it hasn't been fetched before.
        :param skill_name:
        :return:
        """
        skills = self._fetch()
        return skills[skill_name] if skill_name in skills else None

    def fetch_all(self) -> Dict[str, SkillInfo]:
        """
        Fetches Skill info if it hasn't been fetched before.
        :return:
        """
        skills = self._fetch()
        return skills

    def fetch_jobs(self) -> Dict[str, SkillInfo]:
        """
        Fetches Skill info if it hasn't been fetched before.
        :return:
        """
        skills = self._fetch()
        return {name: skill for name, skill in skills.items() if skill.is_job}


interface = SkillInfoFacade(Mapper.mapper)

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from uuid import uuid4
from Tables.Common import Base

class CharacterClass(Base):
    __tablename__ = 'Link_Character_Class'

    character_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    name = Column(String)
    level = Column(Integer)
    number = Column(Integer)
    subclass = Column(String, nullable=True)
    free_book_spells = Column(Integer)
    can_replace_spells = Column(Boolean)
    has_class_choice = Column(Boolean)

    def __repr__(self):
        return f"<CharacterClass(character_id='{self.character_id}', name='{self.name}', level='{self.level}', " \
               f"number='{self.number}', subclass='{self.subclass}', free_book_spells='{self.free_book_spells}', " \
               f"can_replace_spells='{self.can_replace_spells}', has_class_choice='{self.has_class_choice}')>"

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base

from db.models.association import encounter_character, encounter_monster


class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    notes = Column(String)
    characters = relationship(
        "Character", secondary=encounter_character, back_populates="encounters"
    )
    monsters = relationship(
        "Monster", secondary=encounter_monster, back_populates="encounters"
    )

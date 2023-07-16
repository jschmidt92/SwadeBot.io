from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.association import weapon_character, weapon_monster


class Weapon(Base):
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    range = Column(String)
    damage = Column(String)
    rof = Column(Integer)
    shots = Column(Integer)
    min_str = Column(String)
    wt = Column(String)
    cost = Column(Integer)
    notes = Column(String)

    characters = relationship(
        "Character", secondary=weapon_character, back_populates="weapons"
    )
    monsters = relationship(
        "Monster", secondary=weapon_monster, back_populates="weapons"
    )

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.association import gear_character, gear_monster


class Gear(Base):
    __tablename__ = "gear"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    min_str = Column(String)
    wt = Column(String)
    cost = Column(Integer)
    notes = Column(String)

    characters = relationship(
        "Character", secondary=gear_character, back_populates="gear"
    )
    monsters = relationship("Monster", secondary=gear_monster, back_populates="gear")

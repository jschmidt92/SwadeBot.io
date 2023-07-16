from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.association import power_character, power_monster


class Power(Base):
    __tablename__ = "powers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    pp = Column(String)
    range = Column(String)
    duration = Column(String)
    effect = Column(String)
    notes = Column(String)

    characters = relationship(
        "Character", secondary=power_character, back_populates="powers"
    )
    monsters = relationship("Monster", secondary=power_monster, back_populates="powers")

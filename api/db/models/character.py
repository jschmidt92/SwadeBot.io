from sqlalchemy import Column, Integer, String, Enum, JSON
from sqlalchemy.orm import relationship
import enum

from db.base_class import Base
from db.models.association import (
    gear_character,
    power_character,
    weapon_character,
    encounter_character,
    user_characters,
)


class Gender(enum.Enum):
    male = "Male"
    female = "Female"


class Race(enum.Enum):
    android = "Android"
    aquarian = "Aquarian"
    aurax = "Aurax"
    avion = "Avion"
    construct = "Construct"
    deader = "Deader"
    dwarf = "Dwarf"
    elf = "Elf"
    floran = "Floran"
    halfelve = "Half-Elve"
    halffolk = "Half-Folk"
    human = "Human"
    insectoid = "Insectoid"
    kalian = "Kalian"
    rakashan = "Rakashan"
    robot = "Robot"
    saurian = "Saurian"
    serran = "Serran"
    yeti = "Yeti"


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    character_name = Column(String)
    race = Column(Enum(Race), default="human")
    gender = Column(Enum(Gender), default="male")
    charisma = Column(Integer, default=0)
    pace = Column(Integer, default=0)
    parry = Column(Integer, default=0)
    toughness = Column(Integer, default=0)
    attributes = Column(JSON)
    skills = Column(JSON)
    gear = relationship("Gear", secondary=gear_character, back_populates="characters")
    hindrances = Column(String)
    edges = Column(String)
    powers = relationship(
        "Power", secondary=power_character, back_populates="characters"
    )
    weapons = relationship(
        "Weapon", secondary=weapon_character, back_populates="characters"
    )
    damage = Column(JSON, default={"Wounds": 0, "Fatigue": 0, "Inc": "No"})
    ammo = Column(Integer, default=0)
    money = Column(Integer, default=0)
    users = relationship("User", secondary=user_characters, back_populates="characters")
    encounters = relationship(
        "Encounter", secondary=encounter_character, back_populates="characters"
    )

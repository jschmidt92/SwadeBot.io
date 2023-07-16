from sqlalchemy import Column, Integer, String, Enum, JSON
from sqlalchemy.orm import relationship
import enum

from db.base_class import Base
from db.models.association import (
    encounter_monster,
    gear_monster,
    power_monster,
    weapon_monster,
)


class Gender(enum.Enum):
    male = "Male"
    female = "Female"


class Race(enum.Enum):
    android = "Android"
    anklebiter = "Anklebiter"
    angler = "Angler"
    apex = "A-Pex"
    aquarian = "Aquarian"
    aurax = "Aurax"
    avion = "Avion"
    behemoth = "Behemoth"
    bloodwing = "Bloodwing"
    boomer = "Boomer"
    colemata = "Colemata"
    construct = "Construct"
    deader = "Deader"
    deathcrawler = "Death Crawler (Swarm)"
    drake = "Drake"
    dwarf = "Dwarf"
    elf = "Elf"
    floran = "Floran"
    grazer = "Grazer"
    halfelve = "Half-Elve"
    halffolk = "Half-Folk"
    human = "Human"
    hunter = "Hunter"
    insectoid = "Insectoid"
    kalian = "Kalian"
    krok = "Krok"
    krokgiant = "Krok, Giant"
    lightningdarter = "Lightning Darter (Swarm)"
    lacerauns = "Lacerauns"
    mauler = "Mauler"
    rakashan = "Rakashan"
    ravager = "Ravager"
    robot = "Robot"
    sailfin = "Sailfin"
    saurian = "Saurian"
    scrat = "Scrat"
    scuteboar = "Scute Boar"
    serran = "Serran"
    scylla = "Scylla"
    scyllagiant = "Scylla, Giant"
    sirencreeper = "Siren Creeper"
    spitter = "Spitter"
    yeti = "Yeti"


class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True, index=True)
    monster_name = Column(String)
    race = Column(Enum(Race), default="human")
    gender = Column(Enum(Gender), default="male")
    charisma = Column(Integer, default=0)
    pace = Column(Integer, default=0)
    parry = Column(Integer, default=0)
    toughness = Column(Integer, default=0)
    attributes = Column(JSON)
    skills = Column(JSON)
    gear = relationship("Gear", secondary=gear_monster, back_populates="monsters")
    hindrances = Column(String)
    edges = Column(String)
    powers = relationship("Power", secondary=power_monster, back_populates="monsters")
    weapons = relationship(
        "Weapon", secondary=weapon_monster, back_populates="monsters"
    )
    damage = Column(JSON, default={"Wounds": 0, "Fatigue": 0, "Inc": "No"})
    ammo = Column(Integer, default=0)
    money = Column(Integer, default=0)
    encounters = relationship(
        "Encounter", secondary=encounter_monster, back_populates="monsters"
    )

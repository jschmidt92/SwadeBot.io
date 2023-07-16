from sqlalchemy import Enum, Table, Column, Integer, ForeignKey
from db.base_class import Base

gear_character = Table(
    "gear_character",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id")),
    Column("gear_id", Integer, ForeignKey("gear.id")),
    Column("quantity", Integer, default=1),
)

power_character = Table(
    "power_character",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id")),
    Column("power_id", Integer, ForeignKey("powers.id")),
)

weapon_character = Table(
    "weapon_character",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id")),
    Column("weapon_id", Integer, ForeignKey("weapons.id")),
    Column("quantity", Integer, default=1),
)

encounter_character = Table(
    "encounter_character",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id")),
    Column("encounter_id", Integer, ForeignKey("encounters.id")),
)

encounter_monster = Table(
    "encounter_monster",
    Base.metadata,
    Column("monster_id", Integer, ForeignKey("monsters.id")),
    Column("encounter_id", Integer, ForeignKey("encounters.id")),
)

gear_monster = Table(
    "gear_monster",
    Base.metadata,
    Column("monster_id", Integer, ForeignKey("monsters.id")),
    Column("gear_id", Integer, ForeignKey("gear.id")),
    Column("quantity", Integer, default=1),
)

power_monster = Table(
    "power_monster",
    Base.metadata,
    Column("monster_id", Integer, ForeignKey("monsters.id")),
    Column("power_id", Integer, ForeignKey("powers.id")),
)

weapon_monster = Table(
    "weapon_monster",
    Base.metadata,
    Column("monster_id", Integer, ForeignKey("monsters.id")),
    Column("weapon_id", Integer, ForeignKey("weapons.id")),
    Column("quantity", Integer, default=1),
)

user_characters = Table(
    "user_characters",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id")),
    Column("discord_id", Integer, ForeignKey("users.discord_id")),
)

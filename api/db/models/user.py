from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.association import user_characters


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(Integer)
    username = Column(String)

    characters = relationship(
        "Character", secondary=user_characters, back_populates="users"
    )

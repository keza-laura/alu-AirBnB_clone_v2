#!/usr/bin/python3
"""State class"""

from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from models import storage


class State(BaseModel, Base):
    """State class that represents a state"""

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    # DBStorage relationship
    if models.storage_t == 'db':
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete, delete-orphan"
        )

    # FileStorage fallback
    else:
        @property
        def cities(self):
            """Returns list of City objects linked to this State"""
            city_list = []

            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)

            return city_list

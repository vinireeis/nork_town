# Nork_Town
from src.domain.enums.options.enum import ColorOptions, CarModelTypes

# Standards
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class CarModel(Base):
    __tablename__ = "CAR"
    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String(8), nullable=False)
    model = Column(String(15), nullable=False)
    client_id = Column(Integer, nullable=False)

    def __int__(self, color: ColorOptions, model: CarModelTypes, client_id: int):
        self.color = color
        self.model = model
        self.client_id = client_id

    def as_dict(self):
        car = {
            "id": self.id,
            "color": self.color,
            "model": self.model,
            "client_id": self.client_id,
        }
        return car

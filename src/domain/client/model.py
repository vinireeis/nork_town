# Standards
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()


class ClientModel(Base):
    __tablename__ = "CLIENT"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(15), nullable=False)
    email = Column(String(60), nullable=False)
    sale_opportunity = Column(Boolean, nullable=False)

    def __init__(self, name, sale_opportunity, email):
        self.name = name
        self.sale_opportunity = sale_opportunity
        self.email = email

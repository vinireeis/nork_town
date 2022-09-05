from pydantic import BaseModel, constr, Extra
from src.domain.enums.options.enum import ColorOptions, CarModelTypes


class CarValidator(BaseModel):
    color: ColorOptions
    model: CarModelTypes

    class Config:
        extra = Extra.forbid


class ClientValidator(BaseModel):
    name: constr(max_length=60)
    email: constr(max_length=60)
    sale_opportunity: bool = True

    class Config:
        extra = Extra.forbid

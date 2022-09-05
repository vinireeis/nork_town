# nork_town
from src.domain.enums.options.enum import ColorOptions, CarModelTypes
from src.domain.validators.validator import ClientValidator, CarValidator
from src.domain.client.model import ClientModel
from src.domain.cars.model import CarModel


client_payload = {"name": "vini", "email": "vini@123.com"}

car_payload = {"color": ColorOptions.BLUE, "model": CarModelTypes.CONVERTIBLE}

stub_client_payload_validated = ClientValidator(**client_payload)
stub_car_payload_validated = CarValidator(**car_payload)

stub_car_orm_model = [
    CarModel(
        client_id=10,
        color=stub_car_payload_validated.color.value,
        model=stub_car_payload_validated.model.value,
    )
]
stub_client_orm_model = [
    ClientModel(
        name=stub_client_payload_validated.name,
        email=stub_client_payload_validated.email,
        sale_opportunity=stub_client_payload_validated.sale_opportunity,
    )
]

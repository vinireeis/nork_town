# nork_town
from src.domain.enums.options.enum import ColorOptions, CarModelTypes
from src.domain.validators.validator import CustomerValidator, CarValidator
from src.domain.customer.model import CustomerModel
from src.domain.car.model import CarModel


customer_payload = {"name": "vini", "email": "vini@123.com"}

car_payload = {"color": ColorOptions.BLUE, "model": CarModelTypes.CONVERTIBLE}

stub_customer_payload_validated = CustomerValidator(**customer_payload)
stub_car_payload_validated = CarValidator(**car_payload)

stub_car_orm_model = [
    CarModel(
        customer_id=10,
        color=stub_car_payload_validated.color.value,
        model=stub_car_payload_validated.model.value,
    )
]
stub_customer_orm_model = [
    CustomerModel(
        name=stub_customer_payload_validated.name,
        email=stub_customer_payload_validated.email,
        sale_opportunity=stub_customer_payload_validated.sale_opportunity,
    )
]

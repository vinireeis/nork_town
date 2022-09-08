# Nork_Town
from src.domain.validators.validator import CustomerValidator, CarValidator
from src.domain.customer.model import CustomerModel
from src.domain.car.model import CarModel
from src.domain.exceptions.service.exception import CarLimitExceeded, CustomerNotExists, CarNotExists
from src.repositories.sqlite.customer.repository import CustomerRepository
from src.repositories.sqlite.car.repository import CarRepository

# Third party
from decouple import config


class BuyerManagementService:

    customer_repository = CustomerRepository
    car_repository = CarRepository

    @classmethod
    async def register_new_customer(cls, payload_validated: CustomerValidator):
        new_customer = CustomerModel(
            name=payload_validated.name,
            sale_opportunity=payload_validated.sale_opportunity,
            email=payload_validated.email,
        )
        cls.customer_repository.insert_customer(customer=new_customer)
        return True

    @classmethod
    async def linking_car_to_owner(
        cls, payload_validated: CarValidator, customer_id: int
    ) -> bool:
        await cls.check_if_customer_exists(customer_id=customer_id)
        await cls.check_if_customer_can_have_more_cars(customer_id=customer_id)
        color = payload_validated.color.value
        model = payload_validated.model.value
        new_car_linking = CarModel(color=color, model=model, customer_id=customer_id)
        cls.car_repository.insert_car(car=new_car_linking)
        cls.customer_repository.update_sale_opportunity_status(customer_id=customer_id)
        return True

    @classmethod
    async def check_if_customer_can_have_more_cars(cls, customer_id: int):
        cars = cls.car_repository.get_all_cars_per_customer(customer_id=customer_id)
        result = [car for car in cars]
        if len(result) > int(config("CAR_LIMIT")):
            raise CarLimitExceeded()

    @classmethod
    async def check_if_customer_exists(cls, customer_id: int):
        customer = cls.customer_repository.get_customer_by_id(customer_id=customer_id)
        if not customer:
            raise CustomerNotExists()

    @classmethod
    async def check_if_car_exists(cls, car_id: int):
        car = cls.car_repository.get_car_by_id(car_id=car_id)
        if not car:
            raise CarNotExists()

    @classmethod
    async def get_all_customers(cls) -> dict:
        customers = cls.customer_repository.get_all_customer()
        result = {"customers": [customer.as_dict() for customer in customers]}
        return result

    @classmethod
    async def get_all_cars(cls) -> dict:
        cars = cls.car_repository.get_all_cars()
        result = {"car": [car.as_dict() for car in cars]}
        return result

    @classmethod
    async def delete_costumer(cls, customer_id: int):
        await cls.check_if_customer_exists(customer_id=customer_id)
        cls.customer_repository.delete_customer_by_id(customer_id=customer_id)
        return True

    @classmethod
    async def delete_car(cls, car_id: int):
        await cls.check_if_car_exists(car_id=car_id)
        cls.car_repository.delete_car_by_id(car_id=car_id)
        return True

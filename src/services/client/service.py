# Nork_Town
from src.domain.validators.validator import ClientValidator, CarValidator
from src.domain.client.model import ClientModel
from src.domain.cars.model import CarModel
from src.domain.exceptions.service.exception import CarLimitExceeded
from src.repositories.sqlite.repository import SqliteRepository


class ClientService:

    repository = SqliteRepository

    @classmethod
    async def register_new_client(cls, payload_validated: ClientValidator):
        new_client = ClientModel(
            name=payload_validated.name,
            sale_opportunity=payload_validated.sale_opportunity,
            email=payload_validated.email
        )
        cls.repository.insert_client(client=new_client)
        return True

    @classmethod
    async def linking_car_to_owner(cls, payload_validated: CarValidator, client_id: int):
        new_car_linking = CarModel(
            color=payload_validated.color,
            model=payload_validated.model,
            client_id=client_id
        )
        await cls.check_if_client_can_have_more_cars(client_id=client_id)
        cls.repository.insert_car(car=new_car_linking)
        cls.repository.update_sale_opportunity_status(client_id=client_id)
        return True

    @classmethod
    async def check_if_client_can_have_more_cars(cls, client_id: int):
        cars = cls.repository.get_all_cars(client_id=client_id)
        count = 0
        # result = [count + 1 for car in cars] if count < 3 else False
        for car in cars:
            count += 1
        if count > 2:
            raise CarLimitExceeded
        return True




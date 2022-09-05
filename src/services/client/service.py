# Nork_Town
from src.domain.validators.validator import ClientValidator, CarValidator
from src.domain.client.model import ClientModel
from src.domain.cars.model import CarModel
from src.domain.exceptions.service.exception import CarLimitExceeded, ClientNotExists
from src.repositories.sqlite.repository import SqliteRepository

# Third party
from decouple import config


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
    async def linking_car_to_owner(cls, payload_validated: CarValidator, client_id: int) -> bool:
        await cls.check_if_client_exists(client_id=client_id)
        await cls.check_if_client_can_have_more_cars(client_id=client_id)
        color = payload_validated.color.value
        model = payload_validated.model.value
        new_car_linking = CarModel(
            color=color,
            model=model,
            client_id=client_id
        )
        cls.repository.insert_car(car=new_car_linking)
        cls.repository.update_sale_opportunity_status(client_id=client_id)
        return True

    @classmethod
    async def check_if_client_can_have_more_cars(cls, client_id: int):
        cars = cls.repository.get_all_cars_by_id(client_id=client_id)
        result = [car for car in cars]
        if len(result) > int(config("CAR_LIMIT")):
            raise CarLimitExceeded

    @classmethod
    async def check_if_client_exists(cls, client_id: int):
        client = cls.repository.get_client_by_id(client_id=client_id)
        if not client:
            raise ClientNotExists

    @classmethod
    async def get_all_clients(cls):
        clients = cls.repository.get_all_clients()
        result = {
            "clients": [client.as_dict() for client in clients]
        }
        return result

    @classmethod
    async def get_all_cars(cls):
        cars = cls.repository.get_all_cars()
        result = {
            "cars": [car.as_dict() for car in cars]
        }
        return result

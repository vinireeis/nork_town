from src.domain.client.model import ClientModel
from src.domain.cars.model import CarModel
from src.infrastructures.sqlite.infrastructure import SqliteInfrastructure


class SqliteRepository:

    infra = SqliteInfrastructure

    @classmethod
    def insert_customer(cls, client: ClientModel):
        session = cls.infra.get_session()
        session.add(client)
        cls.commit_changes_and_close_session(session=session)

    @classmethod
    def insert_car(cls, car: CarModel):
        session = cls.infra.get_session()
        session.add(car)
        cls.commit_changes_and_close_session(session=session)

    @classmethod
    def update_sale_opportunity_status(cls, client_id: int):
        session = cls.infra.get_session()
        client = session.query(ClientModel).get(client_id)
        client.sale_opportunity = False
        cls.commit_changes_and_close_session(session=session)

    @classmethod
    def get_all_cars_by_id(cls, customer_id: int):
        session = cls.infra.get_session()
        cars = session.query(CarModel).filter(CarModel.client_id == customer_id)
        return cars

    @classmethod
    def get_customer_by_id(cls, customer_id: int):
        session = cls.infra.get_session()
        client = session.query(ClientModel).get(customer_id)
        return client

    @classmethod
    def get_all_customer(cls):
        session = cls.infra.get_session()
        clients = session.query(ClientModel).all()
        return clients

    @classmethod
    def get_all_cars(cls):
        session = cls.infra.get_session()
        clients = session.query(CarModel).all()
        return clients

    @classmethod
    def update_one_customer(cls, customer_updated: ClientModel, customer_id: int):
        session = cls.infra.get_session()
        session.query(ClientModel).get(customer_id).update(customer_updated)
        cls.commit_changes_and_close_session(session=session)

    @staticmethod
    def commit_changes_and_close_session(session):
        session.commit()
        session.close()

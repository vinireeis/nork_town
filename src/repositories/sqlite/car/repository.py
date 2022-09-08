from src.domain.car.model import CarModel
from src.infrastructures.sqlite.infrastructure import SqliteInfrastructure


class CarRepository:

    infra = SqliteInfrastructure

    @staticmethod
    def commit_changes_and_close_session(session):
        session.commit()
        session.close()

    @classmethod
    def insert_car(cls, car: CarModel):
        session = cls.infra.get_session()
        session.add(car)
        cls.commit_changes_and_close_session(session=session)

    @classmethod
    def get_all_cars(cls):
        session = cls.infra.get_session()
        cars = session.query(CarModel).all()
        return cars

    @classmethod
    def get_all_cars_per_customer(cls, customer_id: int):
        session = cls.infra.get_session()
        cars = session.query(CarModel).filter(CarModel.customer_id == customer_id)
        return cars

    @classmethod
    def get_car_by_id(cls, car_id: int):
        session = cls.infra.get_session()
        car = session.query(CarModel).get(car_id)
        return car

    @classmethod
    def delete_car_by_id(cls, car_id: int):
        print(type(car_id))
        session = cls.infra.get_session()
        session.query(CarModel).filter(CarModel.id == car_id).delete()
        cls.commit_changes_and_close_session(session=session)

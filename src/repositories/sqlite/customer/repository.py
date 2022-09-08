from src.domain.customer.model import CustomerModel
from src.infrastructures.sqlite.infrastructure import SqliteInfrastructure


class CustomerRepository:

    infra = SqliteInfrastructure

    @staticmethod
    def commit_changes_and_close_session(session):
        session.commit()
        session.close()

    @classmethod
    def insert_customer(cls, customer: CustomerModel):
        session = cls.infra.get_session()
        session.add(customer)
        cls.commit_changes_and_close_session(session=session)

    @classmethod
    def get_all_customer(cls):
        session = cls.infra.get_session()
        customers = session.query(CustomerModel).all()
        return customers

    @classmethod
    def get_customer_by_id(cls, customer_id: int):
        session = cls.infra.get_session()
        customer = session.query(CustomerModel).get(customer_id)
        return customer

    @classmethod
    def update_sale_opportunity_status(cls, customer_id: int):
        session = cls.infra.get_session()
        customer = session.query(CustomerModel).get(customer_id)
        customer.sale_opportunity = False
        cls.commit_changes_and_close_session(session=session)

    @classmethod
    def update_customer_by_id(cls, customer_updated: CustomerModel, customer_id: int):
        session = cls.infra.get_session()
        session.query(CustomerModel).get(customer_id).update(customer_updated)
        cls.commit_changes_and_close_session(session=session)



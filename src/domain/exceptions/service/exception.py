# Nork_Town
from src.domain.exceptions.base_exceptions.exceptions import ServiceException


class CarLimitExceeded(ServiceException):
    pass


class CustomerNotExists(ServiceException):
    pass

# Nork_Town
from src.domain.validators.validator import CustomerValidator, CarValidator
from src.domain.exceptions.service.exception import CarLimitExceeded, CustomerNotExists, CarNotExists
from src.services.buyer_management.service import BuyerManagementService

# Standards
from json import dumps
from http import HTTPStatus

# Third party
from flask import Flask, Response, request
from loguru import logger

app = Flask("nork_town")


@app.route('/')
async def work_on() -> Response:
    response = {"success": True, "message": "Nork Town API is working"}
    return Response(dumps(response))


@app.route("/customer/register", methods=["POST"])
async def register_new_customer() -> Response:
    try:
        raw_payload = request.json
        payload_validated = CustomerValidator(**raw_payload)
        success = await BuyerManagementService.register_new_customer(
            payload_validated=payload_validated
        )
        response = {"success": success, "message": "buyer_management registered successfully"}
        return Response(dumps(response), status=HTTPStatus.OK)

    except ValueError as ex:
        logger.error(ex)
        response = {"result": False, "message": "Invalid params"}
        return Response(dumps(response), status=HTTPStatus.BAD_REQUEST)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on register new buyer_management"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route("/customer/<int:customer_id>", methods=["DELETE"])
async def delete_one_customer(customer_id: int):
    try:
        success = await BuyerManagementService.delete_costumer(customer_id=customer_id)
        response = {"success": success, "message": "Customer data deleted with successfully"}
        return Response(dumps(response), status=HTTPStatus.OK)

    except CustomerNotExists as ex:
        logger.info(ex)
        response = {"result": False, "message": "Invalid customer id"}
        return Response(dumps(response), status=HTTPStatus.BAD_REQUEST)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on trying to delete car data"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route("/customers")
async def list_all_customers():
    try:
        result = await BuyerManagementService.get_all_customers()
        response = {
            "success": True,
            "result": result,
        }
        return Response(dumps(response), status=HTTPStatus.OK)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on get customers"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route("/linking-car/<int:customer_id>", methods=["POST"])
async def add_new_car_in_customer(customer_id: int) -> Response:
    try:
        raw_payload = request.json
        payload_validated = CarValidator(**raw_payload)
        result = await BuyerManagementService.linking_car_to_owner(
            customer_id=customer_id, payload_validated=payload_validated
        )
        response = {"success": result, "message": "successfully registered car"}
        return Response(dumps(response))

    except CarLimitExceeded as ex:
        logger.info(ex)
        response = {
            "success": False,
            "message": "Customer cannot have more than three car, by Nork Town mayor.",
        }
        return Response(dumps(response), status=HTTPStatus.OK)

    except CustomerNotExists as ex:
        logger.info(ex)
        response = {"result": False, "message": "Customer id invalid."}
        return Response(dumps(response), status=HTTPStatus.BAD_REQUEST)

    except ValueError as ex:
        logger.error(ex)
        response = {"success": False, "message": "Invalid params"}
        return Response(dumps(response), status=HTTPStatus.BAD_REQUEST)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on linking car on the owner"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route("/cars")
async def list_all_cars():
    try:
        result = await BuyerManagementService.get_all_cars()
        response = {
            "success": True,
            "result": result,
        }
        return Response(dumps(response), status=HTTPStatus.OK)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on get car list"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route("/car/<int:car_id>", methods=["DELETE"])
async def delete_one_car(car_id: int):
    try:
        success = await BuyerManagementService.delete_car(car_id=car_id)
        response = {"success": success, "message": "car data deleted with successfully"}
        return Response(dumps(response), status=HTTPStatus.OK)

    except CarNotExists as ex:
        logger.info(ex)
        response = {"result": False, "message": "Car id invalid."}
        return Response(dumps(response), status=HTTPStatus.BAD_REQUEST)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on trying to delete car data"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)

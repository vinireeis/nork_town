# Nork_Town
from src.domain.validators.validator import ClientValidator, CarValidator
from src.domain.exceptions.service.exception import CarLimitExceeded, ClientNotExists
from src.services.client.service import ClientService

# Standards
from json import dumps
from http import HTTPStatus

# Third party
from flask import Flask, Response, request
from loguru import logger

app = Flask("Nork_Town")


@app.route("/client/register", methods=["POST"])
async def register_new_client() -> Response:
    try:
        raw_payload = request.json
        payload_validated = ClientValidator(**raw_payload)
        success = await ClientService.register_new_client(
            payload_validated=payload_validated
        )
        response = {"success": success, "message": "client registered successfully"}
        return Response(dumps(response), status=HTTPStatus.OK)

    except ValueError as ex:
        logger.error(ex)
        response = {"result": False, "message": "Invalid params"}
        return Response(dumps(response), status=HTTPStatus.BAD_REQUEST)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on register new client"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route("/clients")
async def list_all_clients():
    try:
        result = await ClientService.get_all_clients()
        response = {
            "success": True,
            "result": result,
        }
        return Response(dumps(response), status=HTTPStatus.OK)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on get clients"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route("/linking-car/<int:client_id>", methods=["POST"])
async def add_new_car_in_client(client_id: int) -> Response:
    try:
        raw_payload = request.json
        payload_validated = CarValidator(**raw_payload)
        result = await ClientService.linking_car_to_owner(
            client_id=client_id, payload_validated=payload_validated
        )
        response = {"success": result, "message": "successfully registered car"}
        return Response(dumps(response))

    except CarLimitExceeded as ex:
        logger.info(ex)
        response = {
            "success": False,
            "message": "Customer cannot have more than three cars, by Nork Town mayor.",
        }
        return Response(dumps(response), status=HTTPStatus.OK)

    except ClientNotExists as ex:
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
        result = await ClientService.get_all_cars()
        response = {
            "success": True,
            "result": result,
        }
        return Response(dumps(response), status=HTTPStatus.OK)

    except Exception as ex:
        logger.error(ex)
        response = {"success": False, "message": "Error on get cars list"}
        return Response(dumps(response), status=HTTPStatus.INTERNAL_SERVER_ERROR)

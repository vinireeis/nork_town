# nork_town
from src.domain.exceptions.service.exception import CarLimitExceeded, ClientNotExists
from src.services.client.service import ClientService
from tests.src.services.stubs import (
    stub_client_payload_validated,
    stub_car_payload_validated,
    stub_client_orm_model,
    stub_car_orm_model,
)

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch("src.services.client.service.ClientService.repository")
async def test_when_new_client_register_with_successfully_then_return_true(
    mock_repository,
):
    result = await ClientService.register_new_client(
        payload_validated=stub_client_payload_validated
    )

    mock_repository.insert_client.assert_called_once()
    assert result is True


@pytest.mark.asyncio
@patch("src.services.client.service.ClientService.repository")
@patch.object(ClientService, "check_if_client_can_have_more_cars")
@patch.object(ClientService, "check_if_client_exists")
async def test_when_new_linking_car_with_successfully_then_return_true(
    mock_check_client, mock_validate_cars, mock_repository
):
    result = await ClientService.linking_car_to_owner(
        payload_validated=stub_car_payload_validated, client_id=5
    )

    mock_check_client.assert_called_once_with(client_id=5)
    mock_validate_cars.assert_called_once_with(client_id=5)
    mock_repository.insert_car.assert_called_once()
    mock_repository.update_sale_opportunity_status.assert_called_once_with(client_id=5)
    assert result is True


@pytest.mark.asyncio
@patch("src.services.client.service.config", return_value=2)
@patch("src.services.client.service.ClientService.repository")
async def test_when_client_can_have_more_cars_then_proceed(
    mock_repository, mock_decouple
):
    result = await ClientService.check_if_client_can_have_more_cars(client_id=8)

    assert result is None


@pytest.mark.asyncio
@patch("src.services.client.service.config", return_value=2)
@patch(
    "src.services.client.service.ClientService.repository.get_all_cars_by_id",
    return_value=[1, 1, 1],
)
async def test_when_client_exceeded_limit_cars_then_raises(
    mock_repository, mock_decouple
):
    with pytest.raises(CarLimitExceeded):
        await ClientService.check_if_client_can_have_more_cars(client_id=8)


@pytest.mark.asyncio
@patch("src.services.client.service.ClientService.repository")
async def test_when_client_exists_then_proceed(mock_repository):
    result = await ClientService.check_if_client_exists(client_id=7)

    mock_repository.get_client_by_id.assert_called_once_with(client_id=7)
    assert result is None


@pytest.mark.asyncio
@patch(
    "src.services.client.service.ClientService.repository.get_client_by_id",
    return_value=None,
)
async def test_when_client_exists_then_proceed(mock_repository):
    with pytest.raises(ClientNotExists):
        await ClientService.check_if_client_exists(client_id=7)


@pytest.mark.asyncio
@patch(
    "src.services.client.service.ClientService.repository.get_all_clients",
    return_value=stub_client_orm_model,
)
async def test_when_get_all_clients_with_successfully_then_return_expected_result(
    mock_repository,
):
    result = await ClientService.get_all_clients()

    mock_repository.assert_called_once_with()
    assert isinstance(result, dict)


@pytest.mark.asyncio
@patch(
    "src.services.client.service.ClientService.repository.get_all_cars",
    return_value=stub_car_orm_model,
)
async def test_when_get_all_cars_with_successfully_then_return_expected_result(
    mock_repository,
):
    result = await ClientService.get_all_cars()

    mock_repository.assert_called_once_with()
    assert isinstance(result, dict)

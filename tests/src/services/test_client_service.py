# nork_town
from src.domain.exceptions.service.exception import CarLimitExceeded, CustomerNotExists
from src.services.buyer_management.service import BuyerManagementService
from tests.src.services.stubs import (
    stub_customer_payload_validated,
    stub_car_payload_validated,
    stub_customer_orm_model,
    stub_car_orm_model,
)

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch("src.services.buyer_management.service.BuyerManagementService.repository")
async def test_when_new_customer_register_with_successfully_then_return_true(
    mock_repository,
):
    result = await BuyerManagementService.register_new_customer(
        payload_validated=stub_customer_payload_validated
    )

    mock_repository.insert_customer.assert_called_once()
    assert result is True


@pytest.mark.asyncio
@patch("src.services.buyer_management.service.BuyerManagementService.repository")
@patch.object(BuyerManagementService, "check_if_customer_can_have_more_cars")
@patch.object(BuyerManagementService, "check_if_customer_exists")
async def test_when_new_linking_car_with_successfully_then_return_true(
    mock_check_customer, mock_validate_cars, mock_repository
):
    result = await BuyerManagementService.linking_car_to_owner(
        payload_validated=stub_car_payload_validated, customer_id=5
    )

    mock_check_customer.assert_called_once_with(customer_id=5)
    mock_validate_cars.assert_called_once_with(customer_id=5)
    mock_repository.insert_car.assert_called_once()
    mock_repository.update_sale_opportunity_status.assert_called_once_with(customer_id=5)
    assert result is True


@pytest.mark.asyncio
@patch("src.services.buyer_management.service.config", return_value=2)
@patch("src.services.buyer_management.service.BuyerManagementService.repository")
async def test_when_customer_can_have_more_cars_then_proceed(
    mock_repository, mock_decouple
):
    result = await BuyerManagementService.check_if_customer_can_have_more_cars(customer_id=8)

    assert result is None


@pytest.mark.asyncio
@patch("src.services.buyer_management.service.config", return_value=2)
@patch(
    "src.services.buyer_management.service.BuyerManagementService.repository.get_all_cars_by_id",
    return_value=[1, 1, 1],
)
async def test_when_customer_exceeded_limit_cars_then_raises(
    mock_repository, mock_decouple
):
    with pytest.raises(CarLimitExceeded):
        await BuyerManagementService.check_if_customer_can_have_more_cars(customer_id=8)


@pytest.mark.asyncio
@patch("src.services.buyer_management.service.BuyerManagementService.repository")
async def test_when_customer_exists_then_proceed(mock_repository):
    result = await BuyerManagementService.check_if_customer_exists(customer_id=7)

    mock_repository.get_customer_by_id.assert_called_once_with(customer_id=7)
    assert result is None


@pytest.mark.asyncio
@patch(
    "src.services.buyer_management.service.BuyerManagementService.repository.get_customer_by_id",
    return_value=None,
)
async def test_when_customer_exists_then_proceed(mock_repository):
    with pytest.raises(CustomerNotExists):
        await BuyerManagementService.check_if_customer_exists(customer_id=7)


@pytest.mark.asyncio
@patch(
    "src.services.buyer_management.service.BuyerManagementService.repository.get_all_customers",
    return_value=stub_customer_orm_model,
)
async def test_when_get_all_customers_with_successfully_then_return_expected_result(
    mock_repository,
):
    result = await BuyerManagementService.get_all_customers()

    mock_repository.assert_called_once_with()
    assert isinstance(result, dict)


@pytest.mark.asyncio
@patch(
    "src.services.buyer_management.service.BuyerManagementService.repository.get_all_cars",
    return_value=stub_car_orm_model,
)
async def test_when_get_all_cars_with_successfully_then_return_expected_result(
    mock_repository,
):
    result = await BuyerManagementService.get_all_cars()

    mock_repository.assert_called_once_with()
    assert isinstance(result, dict)

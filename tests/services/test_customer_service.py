from psycopg2 import OperationalError
from sqlalchemy.exc import InterfaceError
import pytest

from unittest.mock import MagicMock, patch

from app.exceptions.db_exceptions import TransientDatabaseException
from app.exceptions.service_exceptions import ServiceException
from app.services import CustomerService

@pytest.fixture
def mock_db_manager():
    "Mock database manager for testing."
    manager = MagicMock()
    session_mock = MagicMock()
    manager.transaction.return_value.__enter__.return_value = session_mock
    return manager

@pytest.fixture
def mock_repository():
    "Fixture to mock CustomerRepository."
    return MagicMock()


# Using patch for mocking the sleep function in the retry decorator. Completely disables the wait time during retries. But this is only for testing purposes.
@patch("app.services.CustomerService.register_customer.retry.sleep")
def test_register_customer_success(mock_sleep, mock_db_manager, mock_repository):
    "Test successful customer registration."
    service = CustomerService(db_manager=mock_db_manager, repository=mock_repository)
    mock_repository.save_customer.return_value = {"customer_id": "123", "email": "test@example.com"}
    
    test_data = {"email": "test@example.com", "name": "John Doe"}
    response = service.register_customer(test_data)
    
    assert response["customer_id"] == "123"
    assert mock_repository.save_customer.call_count == 1
    mock_sleep.assert_not_called()
    
@patch("app.services.CustomerService.register_customer.retry.sleep")
def test_register_customer_retry_then_success(mock_sleep, mock_db_manager, mock_repository):
    """
    2. RETRY PATH: Test that transient errors trigger a retry and eventually succeed.
    """
    
    "Test customer registration with retry then success."
    
    service = CustomerService(db_manager=mock_db_manager, repository=mock_repository)
    mock_repository.save_customer.side_effect = [
        OperationalError("Transient database error", None, None),
        InterfaceError("timeout", None, None),
        {"customer_id": "234", "email": "test@example.com"}
    ]
    
    test_data = {"email": "test@example.com", "name": "John Doe"}
    response = service.register_customer(test_data)
    
    assert response["customer_id"] == "234"
    assert mock_repository.save_customer.call_count == 3
    assert mock_sleep.call_count == 2 #Slept between retries
    
@patch("app.services.CustomerService.register_customer.retry.sleep")
def test_register_customer_integrity_error_aborts(mock_sleep, mock_db_manager, mock_repository):
    
    """
    3. INTEGRITY ERROR PATH: Test that unique key / integrity constraints fail immediately 
       without triggering tenacity retries.
    """
    
    service = CustomerService(db_manager=mock_db_manager, repository=mock_repository)
    mock_repository.save_customer.side_effect = Exception("duplicate key value violates unique constraint")
    
    test_data = {"email": "test@example.com", "name": "John Doe"}
    
    with pytest.raises(ServiceException, match="An unexpected error occurred. Please contact the support team."):
        service.register_customer(test_data)
        
    assert mock_repository.save_customer.call_count == 1
    mock_sleep.assert_not_called()
    

@patch("app.services.CustomerService.register_customer.retry.sleep")
def test_register_customer_unexpected_error_raises_service_exception(mock_sleep, mock_db_manager, mock_repository):
    """
    4. UNEXPECTED ERROR PATH: Test that unexpected errors raise a ServiceException immediately.
    """
    service = CustomerService(db_manager=mock_db_manager, repository=mock_repository)
    mock_repository.save_customer.side_effect = RuntimeError("Disk full / memory corrupted")
    
    test_data = {"email": "test@example.com", "name": "John Doe"}
    
    with pytest.raises(ServiceException) as exc_info:
        service.register_customer(test_data)
        
    assert "An unexpected error occurred" in str(exc_info.value)
    assert mock_repository.save_customer.call_count == 1
    mock_sleep.assert_not_called()
    
    
@patch("app.services.CustomerService.register_customer.retry.sleep")    
def test_register_customer_exhaust_retries(mock_sleep, mock_db_manager, mock_repository):
    
    service = CustomerService(db_manager=mock_db_manager, repository=mock_repository)
    mock_repository.save_customer.side_effect = OperationalError("persistent outage")
    
    test_data = {"email": "test@example.com", "name": "John Doe"}
    
    with pytest.raises(TransientDatabaseException) as exc_info:
        service.register_customer(test_data)
        
    assert mock_repository.save_customer.call_count == 3
    assert "persistent outage" in str(exc_info.value)
    assert mock_sleep.call_count == 2 #Slept between retries
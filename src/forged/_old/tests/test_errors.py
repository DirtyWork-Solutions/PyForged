import pytest
import json
import time
from forged.__errors__ import (
    CustomException, PyForgedException, exception_handler, retry, CircuitBreaker,
    failover, ErrorAggregator, ErrorCatalogue
)

def test_custom_exception():
    exc = CustomException("Test error", code=100)
    assert exc.msg == "Test error"
    assert exc.code == 100
    assert exc.is_logged is True

def test_pyforged_exception():
    exc = PyForgedException("PyForged error")
    assert exc.msg == "PyForged error"

def test_exception_handler():
    @exception_handler(default_return="default")
    def faulty_function():
        raise ValueError("An error occurred")

    assert faulty_function() == "default"

def test_retry():
    attempts = 0

    @retry(times=3, delay=0.1)
    def faulty_function():
        nonlocal attempts
        attempts += 1
        raise ValueError("An error occurred")

    assert faulty_function() is None
    assert attempts == 3

# test_circuit_breaker method

def test_circuit_breaker():
    breaker = CircuitBreaker(failure_threshold=2, reset_time=1)

    def faulty_function():
        raise ValueError("An error occurred")

    with pytest.raises(PyForgedException):
        breaker.call(faulty_function)
    with pytest.raises(PyForgedException):
        breaker.call(faulty_function)
    time.sleep(1.5)  # Ensure the reset time has passed
    with pytest.raises(PyForgedException):
        breaker.call(faulty_function)


def test_failover():
    def primary():
        raise ValueError("Primary failed")

    def secondary():
        return "Secondary succeeded"

    assert failover(primary, secondary) == "Secondary succeeded"

def test_error_aggregator():
    aggregator = ErrorAggregator()
    aggregator.add(ValueError("Error 1"))
    aggregator.add(KeyError("Error 2"))

    with pytest.raises(PyForgedException) as exc_info:
        aggregator.raise_if_any()

    assert len(exc_info.value.args[0]) == 2

def test_error_catalogue():
    catalogue = ErrorCatalogue()
    catalogue.add_error("E001", "Error 1")
    assert catalogue.get_error("E001") == "Error 1"

    catalogue.update_error_message("E001", "Updated Error 1")
    assert catalogue.get_error("E001") == "Updated Error 1"

    assert catalogue.error_exists("E001") is True
    assert catalogue.error_exists("E002") is False

    catalogue.remove_error("E001")
    assert catalogue.get_error("E001") == "Unknown error code"

    catalogue.add_error("E002", "Error 2")
    assert catalogue.search_errors_by_message("Error 2") == {"E002": "Error 2"}

    catalogue.add_error_category("E002", "Category1")
    assert catalogue.get_errors_by_category("Category1") == {"E002": "Error 2"}
    assert catalogue.list_categories() == {"Category1"}
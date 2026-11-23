import pytest
from app import validate_product


def test_valid_product_has_no_errors():
    # Arrange
    data = {"title": "Веб-розробка", "price": 5000}

    # Act
    errors = validate_product(data)

    # Assert
    assert errors == []


def test_empty_title_returns_error():
    # Arrange
    data = {"title": "   ", "price": 100}

    # Act
    errors = validate_product(data)

    # Assert
    assert "Поле title обов'язкове" in errors


def test_negative_price_returns_error():
    # Arrange
    data = {"title": "Тест", "price": -50}

    # Act
    errors = validate_product(data)

    # Assert
    assert len(errors) == 1


def test_missing_data_returns_two_errors():
    # Arrange
    data = None

    # Act
    errors = validate_product(data)

    # Assert
    assert len(errors) == 2


@pytest.mark.parametrize("price", [0, 9.99, 1000, 100000])
def test_boundary_and_valid_prices(price):
    # Arrange
    data = {"title": "Послуга", "price": price}

    # Act
    errors = validate_product(data)

    # Assert
    assert errors == []
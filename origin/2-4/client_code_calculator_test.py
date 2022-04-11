import pytest
from client_code_calculator import Calculator


@pytest.fixture
def sample_number():
    number = 2
    return number


def test_calculator(sample_number):
    result = Calculator.calculate(sample_number)

    assert result == 4
import pytest
from client_code_calculator import Calculator


@pytest.fixture
def sample_number():
    number = 2
    return number


def test_calculator(sample_number):
    result = Calculator.calculate(sample_number)

    assert result == 4


def multiply_method_dummy(input_value):
    result = input_value * 5

    return result


@pytest.fixture(autouse=True)
def gh_patched(monkeypatch):
    monkeypatch.setattr(Calculator, "multiply", multiply_method_dummy)
from guardrails import Guard
from validator import SecretsPresent
import pytest


# Instantiate the validator
validator = SecretsPresent(on_fail="exception")


# Test happy path
@pytest.mark.parametrize(
    "value",
    [
        """
        def hello_world():
            print("Hello, World!")
            var_a = "This is not a secret"
            var_b = "This is also not a secret"
        """,
        """
        import guardrails as gd
        import openai
        print("Hello from Guardrails!")
        """,
    ],
)
def test_happy_path(value):
    """Test happy path."""
    guard = Guard.from_string(validators=[validator])
    response = guard.parse(value)
    print("Happy path response", response)
    assert response.validation_passed is True


# Test fail path
@pytest.mark.parametrize(
    "value",
    [
        """
        def hello_world():
            print("Hello, World!")
            usd_api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
            user_password = "password123"
        """,
        """
        import guardrails as gd
        import openai
        print("Hello from Guardrails!")
        var_a = "This is not a secret"
        pwd = "lx123"
        """,
    ],
)
def test_fail_path(value):
    """Test fail path."""
    guard = Guard.from_string(validators=[validator])
    with pytest.raises(Exception):
        response = guard.parse(value)
        print("Fail path response", response)

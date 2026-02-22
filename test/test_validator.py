import concurrent.futures

from guardrails import Guard, OnFailAction
from validator import SecretsPresent
import pytest


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
    guard = Guard().use(SecretsPresent(on_fail=OnFailAction.EXCEPTION))
    response = guard.validate(value)
    assert response.validation_passed is True


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
    guard = Guard().use(SecretsPresent(on_fail=OnFailAction.EXCEPTION))
    with pytest.raises(Exception):
        guard.validate(value)


def test_concurrent_validation():
    """Multiple SecretsPresent instances should not interfere with each other."""

    def validate(text):
        guard = Guard().use(SecretsPresent(on_fail=OnFailAction.NOOP))
        return guard.validate(text)

    inputs = [
        "no secrets here\n",
        "also clean text\n",
        "nothing to see\n",
        "just regular code\n",
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(validate, text) for text in inputs]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert len(results) == 4
    for result in results:
        assert result.validation_passed is True

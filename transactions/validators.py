from decimal import Decimal

from django.core.exceptions import ValidationError

SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP"}
MAX_TRANSACTION_AMOUNT = Decimal("1000000.00")


def parse_amount(raw_amount) -> Decimal:
    try:
        amount = Decimal(str(raw_amount))
    except Exception as exc:  # noqa: BLE001
        raise ValidationError("Amount must be a valid decimal.") from exc
    return amount


def validate_amount(amount: Decimal) -> None:
    if amount <= 0:
        raise ValidationError("Amount must be greater than zero.")
    if amount > MAX_TRANSACTION_AMOUNT:
        raise ValidationError("Amount exceeds the maximum allowed limit.")


def validate_currency(currency: str) -> None:
    if currency.upper() not in SUPPORTED_CURRENCIES:
        raise ValidationError("Currency is not supported.")

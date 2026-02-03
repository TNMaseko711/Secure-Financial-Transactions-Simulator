import json
import uuid

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from transactions.models import Transaction
from transactions.validators import parse_amount, validate_amount, validate_currency


@csrf_exempt
@require_http_methods(["POST"])
def create_transaction(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    try:
        account_id = uuid.UUID(payload.get("account_id", ""))
    except ValueError:
        return JsonResponse({"error": "Invalid account_id."}, status=400)

    idempotency_key = payload.get("idempotency_key")
    if not idempotency_key:
        return JsonResponse({"error": "idempotency_key is required."}, status=400)

    currency = payload.get("currency", "")

    try:
        amount = parse_amount(payload.get("amount"))
        validate_amount(amount)
        validate_currency(currency)
    except ValidationError as exc:
        return JsonResponse({"error": exc.message}, status=400)

    try:
        transaction = Transaction.create_idempotent(
            idempotency_key=idempotency_key,
            account_id=account_id,
            amount=amount,
            currency=currency,
        )
    except ValidationError as exc:
        return JsonResponse({"error": exc.message}, status=400)

    return JsonResponse(
        {
            "id": str(transaction.id),
            "status": transaction.status,
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "hash": transaction.hash,
        },
        status=201,
    )


@require_http_methods(["GET"])
def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if not transaction:
        return JsonResponse({"error": "Transaction not found."}, status=404)

    return JsonResponse(
        {
            "id": str(transaction.id),
            "status": transaction.status,
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "hash": transaction.hash,
            "created_at": transaction.created_at.isoformat(),
        }
    )

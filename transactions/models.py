import hashlib
import uuid

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from transactions.validators import validate_amount, validate_currency


class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        SETTLED = "SETTLED", "Settled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idempotency_key = models.CharField(max_length=128, unique=True)
    account_id = models.UUIDField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    hash = models.CharField(max_length=64, editable=False)
    previous_hash = models.CharField(max_length=64, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gt=0), name="transaction_amount_positive"),
        ]

    def clean(self) -> None:
        validate_amount(self.amount)
        validate_currency(self.currency)

    def save(self, *args, **kwargs):
        if self.pk and Transaction.objects.filter(pk=self.pk).exists():
            raise ValidationError("Transactions are immutable and cannot be edited.")
        self.full_clean()
        self.hash = self.compute_hash()
        super().save(*args, **kwargs)

    def compute_hash(self) -> str:
        payload = f"{self.id}|{self.idempotency_key}|{self.account_id}|{self.amount}|{self.currency}|{self.status}|{self.created_at.isoformat()}|{self.previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @classmethod
    def create_idempotent(cls, *, idempotency_key: str, account_id: uuid.UUID, amount, currency: str) -> "Transaction":
        with transaction.atomic():
            existing = cls.objects.select_for_update().filter(idempotency_key=idempotency_key).first()
            if existing:
                return existing
            instance = cls(
                idempotency_key=idempotency_key,
                account_id=account_id,
                amount=amount,
                currency=currency.upper(),
            )
            instance.save()
            return instance

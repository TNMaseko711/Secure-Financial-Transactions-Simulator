from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("idempotency_key", models.CharField(max_length=128, unique=True)),
                ("account_id", models.UUIDField()),
                ("amount", models.DecimalField(max_digits=12, decimal_places=2)),
                ("currency", models.CharField(max_length=3)),
                (
                    "status",
                    models.CharField(
                        max_length=16,
                        choices=[
                            ("PENDING", "Pending"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                            ("SETTLED", "Settled"),
                        ],
                        default="PENDING",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("hash", models.CharField(max_length=64, editable=False)),
                ("previous_hash", models.CharField(max_length=64, blank=True)),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(check=models.Q(amount__gt=0), name="transaction_amount_positive"),
                ]
            },
        ),
    ]

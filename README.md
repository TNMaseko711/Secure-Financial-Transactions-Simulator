# Secure Financial Transactions Simulator (Flagship)

## What this project proves
This project demonstrates my ability to design and implement **trustworthy, money-adjacent systems** with strong guarantees around data integrity, immutability, and idempotent processing.

## Domain framing
An internal system that **simulates transaction processing** (not a payments UI). It models the back-office engine that validates, records, and processes financial transactions with strict correctness rules.

## Tech stack
- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Security:** Server-side validation + cryptographic hashing for integrity checks

## Core features
- **Transaction creation** with strict server-side validation.
- **Validation rules** for amount boundaries, currency, account status, and policy constraints.
- **Failure scenarios** (e.g., insufficient balance, validation failures, duplicate detection).
- **Idempotent transaction processing** so repeated requests do not create duplicate records.
- **Immutable transaction records** to preserve auditability.

## Explicit constraints
- **No transaction edits** (immutability enforced at the data model layer).
- **Duplicate prevention** via idempotency keys and unique constraints.
- **Transaction status lifecycle** (e.g., `PENDING → APPROVED → SETTLED` or `PENDING → REJECTED`).

## Transaction lifecycle
| Status | Meaning | Allowed transitions |
| --- | --- | --- |
| `PENDING` | Transaction accepted for processing. | `APPROVED`, `REJECTED` |
| `APPROVED` | Validation and policy checks passed. | `SETTLED` |
| `REJECTED` | Validation or policy checks failed. | _terminal_ |
| `SETTLED` | Ledger impact finalized. | _terminal_ |

## Failure scenarios (simulated)
- **Insufficient balance:** Reject when debit exceeds available funds.
- **Invalid currency:** Reject requests outside the configured currency set.
- **Account status violations:** Reject when account is frozen or closed.
- **Duplicate submission:** Return the original transaction from the idempotency key.
- **Policy violations:** Reject on AML or velocity rule failures.

## Idempotency
Idempotency ensures that **retries do not create additional transactions**. Each transaction request carries an **idempotency key** that is stored alongside the immutable record. If the same key is submitted again, the system returns the original transaction outcome instead of creating a duplicate.

**Key guarantees:**
- Exactly one immutable record per idempotency key.
- Replay returns the same transaction status and hash.
- Duplicate detection happens before any ledger impact.

## Data integrity guarantees
The system provides strong integrity guarantees by:
- Enforcing **strict validation** on all writes.
- Storing **immutable records** so audit trails cannot be altered.
- Applying **unique constraints** on idempotency keys.
- Using **hashing** to verify record integrity.
- Recording **append-only corrective entries** instead of edits.

## Why immutability matters in finance
In financial systems, **immutability is foundational**. It prevents tampering, preserves an accurate audit trail, and ensures regulators and stakeholders can trust historical records. Instead of editing transactions, the system records corrective entries, preserving a complete chain of custody for every change.

## Implementation notes (guiding constraints)
- **No edits:** Updates are modeled as new transactions that reference the prior transaction.
- **Idempotency key uniqueness:** Guaranteed at the database layer.
- **Hashing approach:** Transaction rows include a hash of canonicalized fields; optional chaining can include the prior hash for tamper-evidence.
- **Server-side validation only:** Never trust client-provided balances or status flags.

## API overview
### Create transaction
`POST /api/transactions/`

```json
{
  "idempotency_key": "c6f223e3-2b62-4a7c-9a20-5c4a1d4b7809",
  "account_id": "c3c2db3b-4a89-4d88-8ef6-5c78c2f36ad9",
  "amount": "125.00",
  "currency": "USD"
}
```

### Fetch transaction
`GET /api/transactions/<transaction_id>/`

## Local setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure PostgreSQL env vars (defaults shown):
   - `POSTGRES_DB=transactions`
   - `POSTGRES_USER=transactions`
   - `POSTGRES_PASSWORD=transactions`
   - `POSTGRES_HOST=localhost`
   - `POSTGRES_PORT=5432`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

## Status
This README defines the **core guarantees** and behavior for the Secure Financial Transactions Simulator. Implementation will align strictly with these constraints.

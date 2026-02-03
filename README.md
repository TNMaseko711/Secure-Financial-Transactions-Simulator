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

## Idempotency
Idempotency ensures that **retries do not create additional transactions**. Each transaction request carries an **idempotency key** that is stored alongside the immutable record. If the same key is submitted again, the system returns the original transaction outcome instead of creating a duplicate.

## Data integrity guarantees
The system provides strong integrity guarantees by:
- Enforcing **strict validation** on all writes.
- Storing **immutable records** so audit trails cannot be altered.
- Applying **unique constraints** on idempotency keys.
- Using **hashing** to verify record integrity.

## Why immutability matters in finance
In financial systems, **immutability is foundational**. It prevents tampering, preserves an accurate audit trail, and ensures regulators and stakeholders can trust historical records. Instead of editing transactions, the system records corrective entries, preserving a complete chain of custody for every change.

## Status
This README defines the **core guarantees** and behavior for the Secure Financial Transactions Simulator. Implementation will align strictly with these constraints.

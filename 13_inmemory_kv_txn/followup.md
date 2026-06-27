# Follow-up — Bank Ledger with Savepoints

**Mirrors:** Problem 13 (Command/Memento, nested transaction layers, rollback) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design an in-memory bank ledger supporting accounts, transfers, and **nested transactions with savepoints** — apply a batch of operations atomically, or roll back to a savepoint.

## Functional requirements
1. Accounts with balances (integer minor units). Ops: `open(account)`, `deposit(acc, amt)`, `withdraw(acc, amt)`, `transfer(from, to, amt)`.
2. **Invariant**: no account goes negative; a failing op inside a transaction must not partially apply.
3. **Transactions**: `begin()` (nestable), `commit()` (apply the innermost open txn to its parent/ledger), `rollback()` (discard the innermost open txn).
4. **Savepoints**: `savepoint(name)` within a transaction; `rollback_to(name)` undoes ops back to that savepoint without ending the transaction.
5. Reads inside a transaction see its uncommitted effects layered on parent/ledger state; outside readers see only committed state.
6. `balance(acc)` reflects the current transactional view; a `statement(acc)` lists applied operations.

## Non-functional / constraints
- Nested begin/savepoint/rollback correct to arbitrary depth (a stack of diff-layers).
- Single-connection scope unless you add locking — state your scope; sketch how concurrent clients would work (per-account locks) in comments.
- O(1) balance reads; operations don't rescan history.

## Driver scenario
```
open(A); open(B); deposit(A,100)
begin; transfer(A,B,40); balance(A)->60, balance(B)->40
  savepoint(s1); withdraw(B,30); balance(B)->10
  rollback_to(s1); balance(B)->40        # withdraw undone, txn still open
commit; balance(A)->60, balance(B)->40
rollback -> error (no open txn)
```
Also show a transfer that would overdraw is rejected and leaves balances unchanged.

## Edge cases
- `commit`/`rollback`/`rollback_to` with no open txn or unknown savepoint. · Overdraw attempt inside a txn (reject, no partial apply). · Nested savepoints. · Deeply nested begin then single rollback. · Transfer to the same account.

# 02 — Splitwise / Expense Sharing

**Difficulty:** ★★★ · **Asked at:** OpenTable, ShareChat, ClearTax, Groww, Splitwise · **Patterns:** Strategy (split types), graph settlement

## Problem
Model an expense-sharing app. Users in groups add shared expenses; the system tracks who owes whom and can simplify debts.

## Functional requirements
1. Register **users**; create **groups** of users. Users can also transact 1:1 (no group).
2. Add an **expense**: amount, who **paid**, and how it's **split** among participants.
3. Support **3 split strategies**:
   - **EQUAL** — split evenly across participants.
   - **EXACT** — caller specifies each participant's exact share (must sum to the amount).
   - **PERCENT** — caller specifies each participant's percentage (must sum to 100).
4. Maintain a running **balance sheet**: for any user, who they owe and who owes them, and the net amount.
5. `show_balances(user)` and `show_balances_all()`.
6. **Simplify debts / settle up**: given the net balances, produce a **minimal set of transactions** that settles everyone (debt minimization).
7. Record a **settlement** (user A pays user B amount) and update balances.

## Non-functional / constraints
- Money: handle cents correctly — **no floating-point drift** (rounding must still sum to the exact total; decide who absorbs the leftover cent).
- Adding a **new split type** must not touch existing expense logic (Strategy + Open/Closed).
- Validate inputs: EXACT shares sum to total, PERCENT sums to 100, payer/participants exist.

## Driver scenario (your `main()` should show this)
1. Create users U1..U4 in a group.
2. U1 pays 1000 split EQUAL among all 4 → show balances.
3. U1 pays 1200 split EXACT {U1:0, U2:400, U3:400, U4:400}.
4. U4 pays 1000 split PERCENT {U1:40, U2:20, U3:20, U4:20}.
5. `show_balances_all()` → print the full who-owes-whom.
6. Run **simplify** → print the minimal settlement transactions.

## Edge cases to handle
- EXACT not summing to total / PERCENT ≠ 100 → reject. · Rounding (1000 / 3). · Self-payment / payer also a participant. · Settling more than is owed.

## TODO checklist
- [ ] `User`, `Group`, `Expense` entities
- [ ] `SplitStrategy` interface + EQUAL / EXACT / PERCENT impls (with validation)
- [ ] Integer-cents money handling + deterministic leftover-cent rule
- [ ] Balance sheet structure (net pairwise balances)
- [ ] `ExpenseManager` orchestrator: add_expense, show_balances, settle
- [ ] Debt-simplification algorithm (minimize number of transactions)
- [ ] `main()` driver covering the scenario above

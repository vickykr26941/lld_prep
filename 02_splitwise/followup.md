# Follow-up — Multi-Currency Trip Expense Manager

**Mirrors:** Problem 02 (Strategy, graph settlement) · Implement from scratch — no skeleton, no TODOs.

## Problem
Friends on a trip log shared expenses in **different currencies**. Track who owes whom in a chosen **base currency**, and settle up with the fewest transactions.

## Functional requirements
1. Register **users** and a **trip** (group) with a **base currency** (e.g. INR).
2. Add an **expense**: amount + **currency**, who paid, and a split (EQUAL / EXACT / PERCENT). Amounts in foreign currency are converted to base via a **rate provider** at record time.
3. Maintain net pairwise **balances** in the base currency.
4. `show_balances(user)` and `show_balances_all()`.
5. **Simplify debts**: minimal set of base-currency transactions that settle everyone.
6. Record a **settlement** (A pays B) and update balances.
7. The **exchange-rate source is pluggable** (Strategy): a fixed table now; could be a live feed later.

## Non-functional / constraints
- Money in integer **minor units** (cents/paise); no float drift. Currency conversion rounding must be deterministic (state your rule).
- Adding a new split type or rate source must not touch expense logic (Open/Closed).
- Validate: EXACT sums to total, PERCENT = 100, known currency, payer/participants exist.

## Driver scenario
1. Trip with base INR; users U1..U4.
2. U1 pays USD 40 EQUAL among 4; U2 pays EUR 30 EXACT; U3 pays INR 1000 PERCENT.
3. `show_balances_all()` → all in INR.
4. Run simplify → minimal INR settlements.
5. Change the USD→INR rate in the provider and show new expenses use the updated rate (old ones unchanged).

## Edge cases
- Unknown currency. · Conversion rounding leftover. · EXACT/PERCENT validation failures. · Settling more than owed. · Same payer is also a participant.

# 08 — Vending Machine

**Difficulty:** ★★☆ · **Asked at:** Amazon, Microsoft, Adobe · **Patterns:** State, Strategy

## Problem
Design a vending machine: it holds products in slots, accepts coins/notes, dispenses a selected product, and returns change.

## Functional requirements
1. **Inventory**: slots, each with a product (name, price) and a quantity.
2. **State machine** — the machine moves through explicit states:
   `IDLE → COLLECTING_MONEY → DISPENSING → (back to IDLE)`. Behaviour depends on current state (e.g. you can't select a product mid-dispense).
3. Flow: select product → insert money (possibly across multiple inserts) → when inserted ≥ price, **dispense** product and **return change**.
4. **Change-making**: return change using available denominations (greedy is fine; note when exact change is impossible).
5. **Cancel** at any point before dispense → refund everything inserted, back to IDLE.
6. **Refill** inventory and **refill/collect coins** (admin operations).

## Non-functional / constraints
- States and transitions must be **explicit** (State pattern or transition table) — no nested-`if` spaghetti. Invalid actions for a state are rejected cleanly.
- Adding a new state or payment method shouldn't rewrite existing transitions.
- Money handled in integer **cents/smallest-unit** (no float).

## Driver scenario (your `main()` should show this)
1. Load machine: slot A = Coke @ 25 (qty 2), slot B = Water @ 10 (qty 0), denominations stocked.
2. Select Coke, insert 10 + 10 + 10 → dispense Coke, return 5 in change; state back to IDLE.
3. Select Water (qty 0) → rejected "out of stock".
4. Select Coke, insert money, then **cancel** → full refund.
5. Trigger an **exact-change-impossible** case → reject before dispensing and refund.

## Edge cases to handle
- Insert money before selecting (or vice-versa — your call, but be consistent). · Out-of-stock slot. · Insufficient funds (wait for more). · Can't make exact change. · Action invalid for current state.

## TODO checklist
- [ ] `Product`, `Slot`/inventory, `Coin`/denomination model (cents)
- [ ] `VendingMachineState` interface (or enum + transition table) with state-specific behaviour
- [ ] States: Idle, CollectingMoney, Dispensing (+ transitions)
- [ ] Change-making logic + "no exact change" handling
- [ ] `VendingMachine` context: select / insert / cancel / dispense / refill
- [ ] `main()` driver covering the scenario above

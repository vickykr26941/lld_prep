# Follow-up — ATM Machine

**Mirrors:** Problem 08 (State pattern, transitions, dispensing/denominations) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design the control software for an ATM: a user inserts a card, authenticates, and performs transactions (balance, withdraw, deposit); the machine dispenses cash from available denominations.

## Functional requirements
1. **State machine**: `IDLE → CARD_INSERTED → AUTHENTICATED → TRANSACTING → DISPENSING → (eject, back to IDLE)`. Actions are only valid in the right state.
2. Flow: insert card → enter PIN (authenticate, limited attempts → block card) → select account → choose operation.
3. Operations: **check balance**, **withdraw** (debit account, dispense cash), **deposit** (credit account).
4. **Cash dispensing**: compute notes from available denominations (e.g. 2000/500/100); reject if the machine can't make the exact amount or has insufficient cash, **before** debiting.
5. **Cancel / eject card** at (almost) any point → return card, back to IDLE.
6. Track the machine's cash inventory and each account's balance.

## Non-functional / constraints
- States and transitions are explicit (State pattern or transition table); invalid actions rejected cleanly.
- Money in integer minor units; no float.
- Withdrawal must be **atomic**: debit and dispense both succeed, or neither does.
- Adding a new operation or state shouldn't rewrite existing transitions.

## Driver scenario
1. Load the ATM with cash {2000×5, 500×10, 100×20} and accounts.
2. Insert card, wrong PIN twice then correct → authenticated.
3. Check balance; withdraw 2600 → dispense {2000×1, 500×1, 100×1}, balance debited; eject.
4. Withdraw an amount the machine can't make exactly → rejected, no debit.
5. Three wrong PINs on a card → card blocked.

## Edge cases
- Action invalid for current state. · Insufficient account balance. · Insufficient/!exact machine cash. · Card blocked after N failed PINs. · Cancel mid-transaction (no partial debit). · Eject without taking card (timeout → retain card).

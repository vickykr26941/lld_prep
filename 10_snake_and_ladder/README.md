# 10 — Snake & Ladder Game

**Difficulty:** ★★☆ · **Asked at:** Amazon, Microsoft, common warm-up · **Patterns:** OOP modelling, Factory, Strategy (dice)

## Problem
Design the engine for a configurable Snake & Ladder board game for N players.

## Functional requirements
1. A **board** of configurable size (default 100 cells).
2. **Snakes** (head → smaller tail) and **ladders** (bottom → higher top), configurable. A cell can't be both a snake-head and a ladder-bottom.
3. **N players** (≥2), take **turns** in order. Each turn: roll dice, advance; if landing on a snake-head slide down, on a ladder-bottom climb up.
4. **Dice** is pluggable (Strategy): standard 1×d6, or configurable (e.g. 2 dice, or a seeded/deterministic dice for tests).
5. **Win condition**: reach the final cell **exactly**. If a roll would overshoot the last cell, the player **stays put** (or your stated rule — be explicit).
6. **Bonus roll on a 6** (optional, but state your rule).
7. Game runs turn-by-turn until someone wins; report the **winner** and (optionally) the move log.

## Non-functional / constraints
- **Deterministic for tests** — inject a seeded/scripted dice so a game can be replayed exactly. Don't call `random` un-seeded deep inside.
- Adding a different board config or dice variant must not touch the turn-loop logic.
- Clean separation: Board (geometry) vs Game (turn orchestration) vs Player vs Dice.

## Driver scenario (your `main()` should show this)
1. Build a 100-cell board with a few snakes `{16:6, 47:26, 49:11, 56:53, 62:19}` and ladders `{1:38, 4:14, 9:31, 21:42, 28:84}`.
2. Two players, **scripted dice** (fixed roll sequence) so the outcome is deterministic.
3. Run the game; print each move: player, roll, from → to, and any snake/ladder jump.
4. Print the winner.
5. Show the **exact-finish** rule firing at least once (a roll that overshoots → stay).

## Edge cases to handle
- Overshoot the final cell. · Snake-head == ladder-bottom (reject at config time). · Multiple players on the same cell (allowed). · Bonus-6 chaining (cap it?). · Single move that hits a ladder then... (no chaining of snake→ladder unless you decide so — state it).

## TODO checklist
- [ ] `Board` with snakes/ladders config + validation; `next_position(pos)` resolving jumps
- [ ] `Dice` interface + standard and scripted/seeded impls
- [ ] `Player` (id, position)
- [ ] `Game` turn loop: roll → move → resolve jump → check win; exact-finish rule
- [ ] Move log / per-turn trace
- [ ] `main()` driver covering the scenario above (deterministic)

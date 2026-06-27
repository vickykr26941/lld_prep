# Follow-up — Connect Four (Generalized Connect-N)

**Mirrors:** Problem 10 (OOP modelling, Strategy, configurable rules) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design a configurable Connect Four game engine for two players on a vertical grid, generalized to **connect-N** on an `R × C` board.

## Functional requirements
1. A board of configurable **rows × cols** (default 6×7) and a **win length N** (default 4).
2. Two players take **turns** dropping a disc into a **column**; the disc falls to the lowest empty cell of that column.
3. **Win detection**: N in a row horizontally, vertically, or diagonally → that player wins. Make win-checking efficient (check around the last move, not the whole board).
4. **Draw** when the board fills with no winner.
5. The game runs turn-by-turn until win or draw; report the result and a move log.
6. **Move validation**: reject a drop into a full or out-of-range column; reject moves after game over.
7. (Bonus) a pluggable move source (Strategy): scripted moves for deterministic tests vs interactive input.

## Non-functional / constraints
- Board geometry, win-check, and turn orchestration are cleanly separated.
- Win-detection generalizes to any N without rewriting the loop.
- Deterministic for tests via a scripted move sequence (no un-seeded randomness in the engine).

## Driver scenario
1. Standard 6×7 board, N=4, two players, **scripted** column drops.
2. Play a sequence where player 1 gets four diagonally → engine declares the winner and the winning line.
3. Reject a drop into a full column and a move after game over.
4. Run a different config (5×5, N=3) and show a vertical win.
5. Play to a full board with no winner → draw.

## Edge cases
- Drop into a full column / out-of-range column. · Win on the very last cell (win vs draw precedence). · Diagonal wins in both directions. · N larger than the board (no win possible). · Move after game over.

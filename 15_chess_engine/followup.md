# Follow-up — Checkers (Draughts) Engine

**Mirrors:** Problem 15 (Strategy/per-piece rules, Factory, State, legal-move generation) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design a two-player checkers (draughts) engine on an 8×8 board: model pieces and moves, enforce mandatory captures and multi-jumps, handle kinging, and detect game over.

## Functional requirements
1. 8×8 board, pieces only on dark squares; two colors. Piece types: **MAN** and **KING** (polymorphic move rules).
2. Moves: a MAN moves diagonally forward one square to an empty square; **captures** by jumping an adjacent opponent piece into the empty square beyond.
3. **Multi-jump**: after a capture, if the same piece can capture again it **must continue** in the same turn.
4. **Mandatory capture rule**: if any capture is available, the player must play a capturing move (state your variant).
5. **Kinging**: a MAN reaching the far row becomes a KING (can move/capture backward too).
6. Validate it's the player's turn; reject illegal moves with a reason.
7. **Game over**: a player with no pieces or no legal moves loses; report winner. Track move history.

## Non-functional / constraints
- Per-piece move/capture rules are polymorphic — no giant `switch(pieceType)` in the board.
- Legal-move generation is reused by both validation and game-over detection (no duplicated rules).
- Clean separation: Board (state) vs Piece (rules) vs Game (turns/result) vs Move.

## Driver scenario
1. Start position; print the board.
2. Play legal simple moves; turns alternate.
3. Set up a forced capture and show a non-capturing move is **rejected** (mandatory capture).
4. Execute a **double jump** in one turn.
5. Promote a MAN to KING at the far row; show it can now capture backward.
6. Drive a position where a player has no moves → engine declares the winner.

## Edge cases
- Move when not your turn. · Capture available but non-capture attempted (reject). · Multi-jump continuation forced. · King vs man movement directions. · No legal move (loss) vs no pieces (loss). · Jump off the board edge.

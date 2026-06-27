# 15 — Chess Game Engine

**Difficulty:** ★★★★ · **Asked at:** Amazon, Microsoft, Google · **Patterns:** Strategy (move rules), Factory, State

## Problem
Design a two-player chess engine: model the board and pieces, validate moves per piece rules, detect check/checkmate, and run a game.

## Functional requirements
1. 8×8 **board** with the standard starting position. **Pieces**: King, Queen, Rook, Bishop, Knight, Pawn — each with its own movement rule (polymorphism / per-piece **move strategy**).
2. `move(from, to)` for the player to move: validate it's legal (piece's movement, path not blocked, can't capture own piece, must be that player's turn).
3. **Captures** remove the opponent piece.
4. **Check detection**: a move that leaves *your own* king in check is illegal. Detect when the opponent is **in check**.
5. **Checkmate / stalemate** detection → game over with result.
6. **Special moves**: castling, en-passant, pawn **promotion**. (Implement at least promotion + castling; state which you covered.)
7. Track **turn order** (White then Black) and a move history.

## Non-functional / constraints
- Adding/altering a piece's movement must touch only that piece (Open/Closed via per-piece rule objects) — no giant `switch(pieceType)` in the board.
- Legal-move generation should be reused by both move-validation and checkmate detection (don't duplicate the rules).
- Clean separation: Board (state) vs Piece (rules) vs Game (turns/result) vs Move (value object).

## Driver scenario (your `main()` should show this)
1. Start a game; print the board.
2. Play a short legal opening (e.g. `e2e4 e7e5 g1f3 ...`) → board updates, turns alternate.
3. Reject an illegal move (e.g. moving through a piece, or moving into check) with a clear reason.
4. Demonstrate a **capture**.
5. Drive a known **checkmate** sequence (e.g. Fool's/Scholar's mate) → engine reports checkmate + winner.

## Edge cases to handle
- Move when it's not your turn. · Pinned piece (moving it exposes own king → illegal). · King can't move into an attacked square. · Pawn promotion choice. · Castling through/into check or after the king/rook moved. · Stalemate (no legal move but not in check) ≠ checkmate.

## TODO checklist
- [ ] `Color`, `Position`/`Square`, `Move` value types
- [ ] `Piece` base + per-piece move generation (King/Queen/Rook/Bishop/Knight/Pawn)
- [ ] `Board`: state, apply/undo move, path-blocking, square-under-attack query
- [ ] Legal-move filter (can't leave own king in check) reused by check/mate detection
- [ ] Check / checkmate / stalemate detection
- [ ] At least promotion + castling special moves
- [ ] `Game`: turns, history, result; `main()` driver covering the scenario above

# Follow-up — Vector Drawing Canvas with Undo/Redo

**Mirrors:** Problem 14 (Command, Memento, inverse-op undo) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design the editing model for a vector drawing app: users add, move, resize, delete, and group shapes on a canvas, with **unlimited undo/redo**.

## Functional requirements
1. A canvas holds **shapes** (rectangle, circle, line) each with an id and properties (position, size, z-order, color).
2. Operations: `add(shape)`, `delete(id)`, `move(id, dx, dy)`, `resize(id, w, h)`, `set_color(id, color)`, `group(ids)` / `ungroup(group_id)`, `bring_to_front(id)`.
3. **Undo** reverts the last operation; **Redo** re-applies it. Support **unlimited** depth (or a configurable cap).
4. A new edit after an undo **clears the redo stack**.
5. Each operation is a **Command** with `execute()` / `undo()` storing the inverse — not a full-canvas snapshot per edit.
6. **Composite group**: moving a group moves all members; undo of a group move reverts all of them as one unit.
7. (Bonus) coalesce a continuous drag (many small moves) into a single undo unit.

## Non-functional / constraints
- Undo/redo cost is O(operation size), not O(canvas size).
- Adding a new operation type means adding a Command, not editing the editor (Open/Closed).
- Shape state stays valid after every op (ids unique, group membership consistent).

## Driver scenario
1. Add rect R1 and circle C1; print canvas.
2. Move R1 by (10,0); resize C1 → undo twice restores both; redo re-applies.
3. After an undo, add a new shape → redo stack cleared (redo is a no-op).
4. Group {R1, C1}, move the group, then undo → both members revert together.
5. (If coalescing) a drag of R1 across 5 small moves undoes as one.

## Edge cases
- Undo/redo with empty stacks (no-op). · Delete then undo (shape + its z-order restored). · Group/ungroup undo consistency. · Move/resize an unknown id. · Redo invalidated by a new edit.

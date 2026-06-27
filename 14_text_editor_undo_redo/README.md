# 14 — Text Editor with Undo / Redo

**Difficulty:** ★★★★ · **Asked at:** Google, Microsoft, Adobe (senior) · **Patterns:** Command, Memento

## Problem
Design the core of a text editor's editing model: insert/delete/replace text with a cursor, plus **unlimited undo/redo**.

## Functional requirements
1. A document holds text + a **cursor** position (and optionally a selection range).
2. Operations: `insert(text)` at cursor, `delete(n)` (backspace n chars), `replace(range, text)`, `move_cursor(pos)`, `select(start, end)`.
3. **Undo** reverts the last operation; **Redo** re-applies the last undone op. Support **unlimited** depth (or a configurable cap).
4. A **new edit after an undo clears the redo stack** (standard editor behaviour).
5. Each operation is a **Command** with `execute()` / `undo()` (or a **Memento** snapshot — pick and justify; Command is more memory-efficient than full snapshots).
6. (Senior bonus) **Coalescing**: consecutive single-char inserts merge into one undo unit (typing "hello" undoes as one word, not 5 chars). Make the policy pluggable.

## Non-functional / constraints
- Undo/redo must be **O(edit size)**, not O(document size) — don't snapshot the whole document per keystroke if you can store the inverse op (this is the key senior signal).
- The text buffer should handle large docs reasonably — naive string concatenation is O(n) per edit; note (or implement) a **gap buffer / piece table / rope** as the level-up.
- Cursor/selection must stay valid after every op (clamp to bounds).

## Driver scenario (your `main()` should show this)
1. Insert "Hello", insert " World" → doc = "Hello World".
2. `delete(6)` → "Hello". Undo → "Hello World". Undo → "Hello". Redo → "Hello World".
3. After an undo, type new text → redo stack is cleared (redo now a no-op).
4. (If coalescing) type "abc" char-by-char, one undo removes all three.
5. Print the document + cursor after each step.

## Edge cases to handle
- Undo/redo with empty stacks (no-op, not crash). · Delete more chars than exist (clamp). · Cursor at start/end bounds. · Redo invalidated by a new edit. · Replace over a selection then undo.

## TODO checklist
- [ ] Document model: text buffer + cursor (+ selection)
- [ ] `Command` interface: `execute()` / `undo()` for Insert / Delete / Replace
- [ ] Undo stack + redo stack with the "new edit clears redo" rule
- [ ] Inverse-op storage (avoid whole-doc snapshots)
- [ ] (Bonus) coalescing policy for consecutive typing
- [ ] `main()` driver covering the scenario above

# Follow-up — Warehouse Robot Dispatch

**Mirrors:** Problem 04 (State, Strategy, dispatch) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design the controller for a fleet of warehouse robots on a grid. Pick-up/drop-off tasks arrive; the controller dispatches robots to carry items from a source cell to a destination cell.

## Functional requirements
1. A `W × H` grid; **R robots**, each at a cell with a **state**: `IDLE`, `MOVING_TO_PICKUP`, `CARRYING`, `MOVING_TO_DROP`, `CHARGING`.
2. A **task**: `(source cell, destination cell)`. Tasks queue up when no robot is free.
3. A **dispatch strategy** (Strategy) assigns a task to a robot: nearest-idle robot (Manhattan distance), or most-charged robot — pluggable.
4. `tick()` advances the simulation one unit: each busy robot moves one cell toward its target, picks up at source, drops at destination, then returns to IDLE.
5. Robots have a **battery**; below a threshold they route to a charging station (state `CHARGING`) instead of taking tasks.
6. Each robot orders its path sensibly (no thrash); two robots must not occupy the same cell at the same tick (collision avoidance — state your rule).

## Non-functional / constraints
- Dispatch strategy is swappable without touching robot/movement code.
- State transitions are explicit (State pattern or transition table); no `if`-soup.
- Deterministic via `tick()` — no wall-clock sleeps.

## Driver scenario
1. 5×5 grid, 2 robots at corners, both IDLE.
2. Submit task A (pickup (0,1) → drop (4,4)) → dispatch picks a robot; print which and why.
3. Submit task B while both robots are busy → it queues.
4. Run `tick()` loop printing each robot's cell + state until both tasks complete.
5. Drop a robot's battery below threshold → it diverts to charging and refuses new tasks.

## Edge cases
- Source == destination. · No idle robot (queue). · Two robots targeting adjacent cells (collision). · Task to an unreachable/occupied cell. · Battery depletes mid-task.

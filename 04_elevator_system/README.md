# 04 — Elevator System

**Difficulty:** ★★★ · **Asked at:** Amazon, Microsoft, Uber, Google, Adobe · **Patterns:** State, Strategy

## Problem
Design the control system for a building with **multiple elevators**. Handle external hall calls (up/down on a floor) and internal car requests (go to floor), and dispatch elevators efficiently.

## Functional requirements
1. Building has **F floors** and **E elevators**.
2. Two request sources:
   - **External / hall call**: `(floor, direction)` — someone on floor 7 presses "down".
   - **Internal / car call**: `(elevator_id, target_floor)` — a rider inside picks a floor.
3. Each elevator is a **state machine**: `IDLE`, `MOVING_UP`, `MOVING_DOWN`, `DOORS_OPEN` (optionally `MAINTENANCE`).
4. A **dispatch strategy** decides which elevator serves a hall call. Support at least:
   - **Nearest / shortest-seek** (pick the closest suitable elevator), and
   - **SCAN / LOOK** (elevator keeps direction, serving requests along the way).
5. `step()` / `tick()` advances simulation by one time unit: elevators move one floor, open/close doors, serve & drop pending stops.
6. An elevator serving requests must order stops sensibly in its current direction (not FCFS thrash).

## Non-functional / constraints
- **Strategy is pluggable** — swapping the dispatch algorithm must not touch elevator/movement code.
- **State transitions are explicit** — model them as a State pattern or an explicit transition table; no tangled `if` soup.
- Deterministic simulation via `tick()` (no wall-clock sleeps) so it's testable.

## Driver scenario (your `main()` should show this)
1. Building: 10 floors, 2 elevators, both start IDLE at floor 0.
2. Hall call: floor 5 UP → dispatch picks an elevator; print which and why.
3. Rider inside that elevator presses floor 9 (internal request).
4. Hall call: floor 3 DOWN.
5. Run `tick()` in a loop and **print each elevator's floor + state** per tick until all requests served.
6. Show that the SCAN strategy serves in-path stops in order.

## Edge cases to handle
- Request for the floor the elevator is already on. · All elevators busy / moving away. · Up and down calls on the same floor. · Idle tie-break (two equally-close elevators).

## TODO checklist
- [ ] `Direction`, `ElevatorState` enums
- [ ] `Request` (hall vs car) modelling
- [ ] `Elevator` with state transitions + sorted pending stops
- [ ] `DispatchStrategy` interface + Nearest and SCAN/LOOK impls
- [ ] `ElevatorController` (registers requests, runs dispatch, drives `tick()`)
- [ ] `main()` driver with the per-tick trace

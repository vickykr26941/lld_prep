# Learning LLD — Low-Level Design in Python

A self-practice repo of the **top 10 mid/senior-level LLD (machine-coding) interview questions**.

**The deal:**
- Each problem folder ships with a `README.md` (requirements + TODO checklist) and a `solution.py` skeleton that contains **only TODOs** — no implementation.
- **You** design the classes and write the code.
- **I (Claude)** act as the judge: I review your design against the rubric in [`RUBRIC.md`](RUBRIC.md), point out missing requirements, design-pattern misuse, concurrency bugs, SOLID violations, and edge cases — then score it.

**20-day plan:** one problem per day (see [`PROGRESS.md`](PROGRESS.md)). Each day: implement `solution.py` → I judge → then implement that folder's **`followup.md`** (a similar problem, *requirements only — no skeleton*) from scratch as `followup_solution.py` → I judge that too.

## How to use this repo

1. Pick a problem (start with `01_parking_lot`, they get harder).
2. Read its `README.md` fully. Note the functional + non-functional requirements and the driver scenario.
3. Implement your design in that folder's `solution.py` (add more files if you want).
4. When done, tell me **"judge problem N"** and I'll review it.
5. Iterate until it's interview-ready.

## Tier 1 — the core 10 (mid → senior)

| #  | Problem | Core patterns | Difficulty |
|----|---------|---------------|------------|
| 01 | [Parking Lot System](01_parking_lot/) | Strategy, Factory, Singleton | ★★☆ |
| 02 | [Splitwise / Expense Sharing](02_splitwise/) | Strategy, graph settlement | ★★★ |
| 03 | [Rate Limiter](03_rate_limiter/) | Strategy, Factory, concurrency | ★★★ |
| 04 | [Elevator System](04_elevator_system/) | State, Strategy | ★★★ |
| 05 | [LRU / LFU Cache](05_cache/) | Strategy, data-structure design | ★★☆ |
| 06 | [Movie Ticket Booking (BookMyShow)](06_movie_booking/) | Concurrency, locking, Factory | ★★★ |
| 07 | [Logging Framework (log4j-style)](07_logging_framework/) | Chain of Responsibility, Observer | ★★☆ |
| 08 | [Vending Machine](08_vending_machine/) | State, Strategy | ★★☆ |
| 09 | [Notification System](09_notification_system/) | Observer, Strategy, Decorator, Factory | ★★★ |
| 10 | [Snake & Ladder Game](10_snake_and_ladder/) | OOP modelling, Factory | ★★☆ |

## Tier 2 — harder (senior → staff)

Heavier on **concurrency**, non-trivial **algorithms/data structures**, and production concerns. Do Tier 1 first.

| #  | Problem | Core patterns | Difficulty |
|----|---------|---------------|------------|
| 11 | [Thread Pool / Executor Service](11_thread_pool/) | Producer-Consumer, Strategy, Future | ★★★★ |
| 12 | [Task / Job Scheduler](12_task_scheduler/) | Min-heap dispatch, Strategy, concurrency | ★★★★ |
| 13 | [In-Memory KV Store w/ Transactions](13_inmemory_kv_txn/) | Command/Memento, nested-layer stack | ★★★★ |
| 14 | [Text Editor Undo/Redo](14_text_editor_undo_redo/) | Command, Memento | ★★★★ |
| 15 | [Chess Game Engine](15_chess_engine/) | Strategy (move rules), Factory, State | ★★★★ |
| 16 | [Search Autocomplete / Typeahead](16_search_autocomplete/) | Trie, Strategy (ranking), top-K | ★★★★ |
| 17 | [In-Memory File System](17_inmemory_filesystem/) | Composite, path resolution | ★★★★ |
| 18 | [Pub/Sub Message Broker (Kafka-lite)](18_pubsub_message_broker/) | Observer, Producer-Consumer, partitioning | ★★★★★ |
| 19 | [Distributed Cache (Consistent Hashing)](19_distributed_cache/) | Consistent hashing, Strategy, replication | ★★★★★ |
| 20 | [Ride-Hailing / Cab Booking (Uber)](20_ride_hailing/) | State, Strategy, spatial index, concurrency | ★★★★★ |

## Ground rules (interview-realistic)

- **Plain Python stdlib only.** No frameworks, no DB. In-memory state is fine.
- **No `print`-driven logic** — model real classes/interfaces. `print` only for demo output.
- Write a small `if __name__ == "__main__":` **driver** in each `solution.py` that exercises the scenario in the README.
- Aim to "finish" each in **45–60 min** like a real machine-coding round. Then come back and polish.
- Favour **clean abstractions over feature-completeness**. A well-structured partial solution beats a messy complete one.

See [`RUBRIC.md`](RUBRIC.md) for exactly how I'll score each submission.

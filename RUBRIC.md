# Judging Rubric

When you ask me to **"judge problem N"**, I review the code in that folder and score it across 6 dimensions (100 pts). This mirrors how a real machine-coding interviewer evaluates.

| Dimension | Weight | What I look for |
|-----------|:------:|-----------------|
| **1. Requirements coverage** | 25 | Every functional requirement in the README is met. The driver scenario runs and produces correct output. Edge cases handled. |
| **2. Class design & OOP** | 20 | Clear entities, right responsibilities, encapsulation, no god-classes. Enums for fixed sets. Interfaces (ABCs) where polymorphism is needed. |
| **3. Design patterns & extensibility** | 20 | The right patterns applied *where they add value* (not pattern-soup). Easy to add a new strategy/type without touching existing code (Open/Closed). |
| **4. SOLID & code quality** | 15 | SRP, DIP, readable names, no duplication, small methods, typing/`dataclass` used well, no dead code. |
| **5. Concurrency & correctness** | 10 | Thread-safety where the problem demands it (booking, rate limiting, cache). No race conditions; locking at the right granularity. (Skipped for single-threaded problems.) |
| **6. Testability & API** | 10 | Clean public API, dependency injection over globals, deterministic (clock injectable), easy to unit-test. |

### Scoring bands
- **90–100** — Hire / senior bar. Ship-quality, extensible, handles edge cases.
- **75–89** — Solid mid-level. Minor gaps; would pass most rounds.
- **60–74** — Borderline. Core works but design or edge cases weak.
- **< 60** — Needs rework. Missing requirements or structural problems.

### What I'll give you back
1. **Score** per dimension + total.
2. **Top 3 things done well.**
3. **Concrete fixes**, each tagged `[blocker]`, `[major]`, or `[nit]`, with the file:line and a suggested change.
4. **One "level-up" idea** — what would push it from mid to senior.

I will **not** rewrite your solution unless you explicitly ask. The point is for you to design it.

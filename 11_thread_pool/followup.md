# Follow-up — Print Spooler with Priority Queue

**Mirrors:** Problem 11 (Producer-Consumer, worker pool, Strategy, graceful shutdown) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design a print spooler: applications submit print jobs with a **priority**; a fixed pool of printer workers processes them, highest priority first, with cancellation and graceful shutdown.

## Functional requirements
1. Construct with **K printer workers** and a bounded job buffer.
2. `submit(job, priority) -> JobHandle` — returns a handle to check status (`QUEUED`/`PRINTING`/`DONE`/`CANCELLED`/`FAILED`) and wait for completion.
3. Jobs are dispatched **by priority** (then FIFO within a priority) to idle workers — a priority queue, not plain FIFO.
4. Workers process jobs concurrently (≤ K at once); idle workers block, no busy-spin.
5. **Cancel** a queued job (remove before it prints); a job already printing runs to completion (or supports cooperative cancel — state your choice).
6. **Rejection policy** when the buffer is full (Strategy: ABORT / CALLER_PRINTS / DROP_LOWEST).
7. **Shutdown**: `shutdown()` finishes queued jobs then stops; `shutdown_now()` cancels queued jobs and returns them; `await_termination(timeout)`.

## Non-functional / constraints
- Correctness: no lost jobs, no deadlock on shutdown, a failing job doesn't kill its worker.
- Bounded buffer applies backpressure; never unbounded.
- Priority ordering stable (equal priority → FIFO). No busy-wait.

## Driver scenario
1. Pool of 2 workers, buffer 5.
2. Submit jobs with mixed priorities (some HIGH after LOW already queued) → HIGH ones print first.
3. Show ≤2 print concurrently (worker ids / timestamps).
4. Cancel a still-queued job → its handle shows CANCELLED, never printed.
5. One job raises → its handle is FAILED, others unaffected.
6. `shutdown()` then `await_termination()` → all non-cancelled jobs done, workers exited.

## Edge cases
- Submit after shutdown. · Cancel a job that just started printing. · Buffer full → rejection policy fires. · Equal-priority ordering. · `shutdown_now()` returns un-printed jobs.

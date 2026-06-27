# 11 — Thread Pool / Executor Service

**Difficulty:** ★★★★ · **Asked at:** Amazon, Uber, Atlassian (senior) · **Patterns:** Producer-Consumer, Strategy (rejection), Command

## Problem
Build a fixed-size thread pool (like Java's `ExecutorService`) that runs submitted tasks on a bounded set of worker threads, with a task queue, futures, and graceful shutdown.

## Functional requirements
1. Construct with **N worker threads** and a **bounded task queue**.
2. `submit(callable) -> Future` — returns a handle the caller can `result()` (blocking) / check `is_done()`. Exceptions in the task are captured and re-raised from `result()`.
3. Workers pull from the queue (**producer-consumer**) and execute tasks concurrently; idle workers block, they don't busy-spin.
4. **Rejection policy** (Strategy) when the queue is full: `ABORT` (raise), `DISCARD` (drop), `CALLER_RUNS` (run on submitting thread). Pluggable.
5. **Shutdown semantics**:
   - `shutdown()` — stop accepting new tasks, finish queued ones, then exit workers.
   - `shutdown_now()` — stop accepting, drain queue, signal workers to stop ASAP; return un-run tasks.
   - `await_termination(timeout)` — block until all workers exit or timeout.
6. (Senior bonus) Expose simple metrics: active workers, queued count, completed count.

## Non-functional / constraints
- **Correctness is everything**: no lost tasks, no deadlock on shutdown, no worker left blocked on an empty queue after shutdown. Use a poison-pill or a shutdown flag + condition correctly.
- Bounded queue must apply **backpressure** (block or reject per policy), never grow unbounded.
- No busy-waiting. Use `queue.Queue`/`threading.Condition` properly.

## Driver scenario (your `main()` should show this)
1. Pool of 3 workers, queue capacity 5.
2. Submit 10 tasks (each sleeps briefly + returns a value) → collect futures.
3. Show concurrency: ≤3 run at once (print worker ids / timestamps).
4. One task raises → its `future.result()` re-raises the exception; others unaffected.
5. Fill the queue and trigger the **rejection policy** (show CALLER_RUNS vs ABORT).
6. `shutdown()` then `await_termination()` → all submitted tasks completed, workers exited cleanly.

## Edge cases to handle
- Submit after shutdown → rejected. · `shutdown_now()` while tasks queued → returns the un-run ones. · `result()` called before completion → blocks. · Task raising must not kill its worker thread.

## TODO checklist
- [ ] `Future` (result/exception, done event, blocking `result()`)
- [ ] `RejectionPolicy` interface + ABORT / DISCARD / CALLER_RUNS
- [ ] Bounded task queue + worker loop (no busy-wait)
- [ ] `ThreadPool`: submit / shutdown / shutdown_now / await_termination
- [ ] Clean worker termination (poison pill or flag+condition)
- [ ] `main()` driver covering the scenario above

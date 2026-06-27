# 12 — Task / Job Scheduler

**Difficulty:** ★★★★ · **Asked at:** Amazon, Uber, Google (senior) · **Patterns:** Strategy (schedule), Producer-Consumer, Command

## Problem
Design an in-process job scheduler (think a mini Quartz / cron + `setTimeout`). Jobs are scheduled to run at a time, after a delay, or on a recurring interval/cron, and execute on a worker pool.

## Functional requirements
1. `schedule(job, run_at)` — one-shot at an absolute time.
2. `schedule_after(job, delay)` — one-shot after a delay.
3. `schedule_recurring(job, interval)` — fixed-rate repeating; and/or a simple **cron** ("every minute", "at HH:MM"). Recurrence behind a **Strategy** so new schedule types plug in.
4. A **single dispatcher thread** sleeps until the **earliest** due job (min-heap / priority queue by next-run time) — O(1) wakeups regardless of queue size, **not** a per-job thread, **not** a busy poll.
5. When a job is due, it's handed to a **worker pool** to execute (don't run jobs on the dispatcher thread).
6. `cancel(job_id)` — cancel a scheduled/recurring job.
7. Recurring jobs **re-enqueue** their next occurrence after firing.
8. **Deterministic** via an injectable clock + a controllable "advance time" so tests don't wait in real time.

## Non-functional / constraints
- Adding a new job to the front of the heap must **wake the sleeping dispatcher** early (condition variable, not fixed-interval polling).
- Thread-safe heap operations; no missed or double-fired jobs.
- A failing job must not crash the dispatcher or stop other jobs; support a **retry** policy (optional).
- Misfire handling: if the scheduler was busy/asleep and a job is late, decide run-now vs skip (state your rule).

## Driver scenario (your `main()` should show this)
1. Schedule job A after 100 (units), B after 50, C recurring every 30.
2. Drive the injected clock forward; print fire order → **B, then C, then A**, with C firing repeatedly.
3. Add job D after 10 *while* the dispatcher is "asleep waiting for B" → it wakes early and fires D first.
4. `cancel(C)` → it stops recurring.
5. A job raises → logged, retried per policy, others unaffected.

## Edge cases to handle
- Two jobs due at the same instant (stable tie-break). · Cancel a job mid-flight. · Scheduling in the past (run immediately?). · Recurring interval shorter than execution time (overlap policy). · Empty queue → dispatcher waits, doesn't spin.

## TODO checklist
- [ ] `Job`/`ScheduledTask` (id, callable, next-run, schedule strategy)
- [ ] `ScheduleStrategy` interface: one-shot / fixed-rate / cron → `next_run(after)`
- [ ] Min-heap priority queue by next-run time + thread-safe access
- [ ] Dispatcher thread: sleep-until-due with early wakeup on new/earlier job
- [ ] Worker pool to execute due jobs (reuse your Problem 11 design if you like)
- [ ] Injectable clock + cancel + retry-on-failure
- [ ] `main()` driver covering the scenario above

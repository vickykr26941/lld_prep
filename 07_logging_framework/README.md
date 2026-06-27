# 07 — Logging Framework (log4j-style)

**Difficulty:** ★★☆ · **Asked at:** Atlassian, Amazon, Microsoft · **Patterns:** Chain of Responsibility, Strategy, Observer/Factory

## Problem
Design a configurable logging library (like log4j / Python `logging`). Code emits log messages at levels; the framework formats and routes them to one or more destinations based on configuration.

## Functional requirements
1. **Levels** with ordering: `DEBUG < INFO < WARN < ERROR < FATAL`.
2. A `Logger.log(level, message)` (plus `debug()/info()/warn()/error()/fatal()` helpers).
3. A configurable **minimum level**: messages below it are dropped. (Model the level-threshold filtering — a Chain of Responsibility of handlers, or a level check per appender.)
4. **Appenders / sinks** (pluggable): at least **Console** and **File** (file can be simulated with an in-memory buffer). A logger can have **multiple** appenders → a message fans out to all.
5. **Formatter / layout** is pluggable: e.g. `"[{level}] {timestamp} {message}"`. Swapping format must not touch appenders.
6. Each **appender** can have its **own** min-level (e.g. console shows INFO+, file captures DEBUG+).

## Non-functional / constraints
- Adding a new appender (e.g. network/syslog) or a new formatter must require **zero changes** to existing code (Open/Closed).
- **Thread-safe** logging (multiple threads logging concurrently shouldn't interleave a single line).
- Timestamp via an **injectable clock** for deterministic tests.
- (Senior bonus) Note how you'd make logging **async / non-blocking** without losing messages.

## Driver scenario (your `main()` should show this)
1. Build a logger with two appenders: Console (min INFO) + File-buffer (min DEBUG), shared formatter.
2. Log one message at each level.
3. Show DEBUG appears only in the file buffer, INFO+ in both, and a sub-threshold message is dropped.
4. Swap the formatter to a different layout and log again → output format changes, code unchanged.

## Edge cases to handle
- Level exactly at threshold (inclusive?). · Logger with no appenders. · Appender failure shouldn't crash the caller / block other appenders. · Concurrent writes.

## TODO checklist
- [ ] `LogLevel` enum with ordering + a `LogMessage`/record type
- [ ] `Formatter` interface + ≥1 layout
- [ ] `Appender` interface + Console and File(buffer) impls, each with own min-level
- [ ] Level filtering (Chain of Responsibility or per-appender check)
- [ ] `Logger` fanning out to appenders, thread-safe, injectable clock
- [ ] `main()` driver covering the scenario above

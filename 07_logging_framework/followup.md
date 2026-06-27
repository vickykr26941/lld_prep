# Follow-up — Alerting & Monitoring System

**Mirrors:** Problem 07 (Chain of Responsibility, Strategy, Observer, pluggable sinks) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design a monitoring system: metrics stream in; **rules** evaluate them and raise **alerts** at a severity; alerts are routed and delivered to notification channels based on severity and configuration.

## Functional requirements
1. Ingest **metric samples**: `(metric_name, value, timestamp)`.
2. **Alert rules** (pluggable, Strategy): e.g. threshold (`cpu > 90`), or rate-of-change, evaluated on incoming samples. A breached rule raises an **Alert** with a **severity** (`INFO < WARN < CRITICAL`).
3. **Routing**: each channel (Console, Email, PagerDuty-sim) has a **minimum severity** — an alert fans out only to channels that accept its severity (like log appenders by level).
4. **Deduplication / suppression**: don't re-fire the same alert while it's still firing; emit a **resolve** when the metric returns to normal.
5. **Formatter** per channel is pluggable.
6. Severity filtering modeled as a chain or per-channel check.

## Non-functional / constraints
- Adding a new rule type, channel, or formatter requires zero changes elsewhere (Open/Closed).
- Thread-safe ingestion (multiple producers) — an alert delivery failing on one channel must not block others.
- Timestamps/cooldowns via an **injectable clock**.

## Driver scenario
1. Rule: `cpu > 90` → CRITICAL. Channels: Console (min INFO), Email (min WARN), Pager (min CRITICAL).
2. Feed cpu = 95 → alert fires to all three; feed cpu = 96 again → suppressed (no duplicate).
3. Feed cpu = 50 → a **resolve** is emitted.
4. Add a WARN-severity rule and show it reaches Console + Email but not Pager.
5. Swap a channel's formatter and show output format changes, code unchanged.

## Edge cases
- Metric exactly at threshold (inclusive?). · No channel accepts an alert's severity. · Flapping metric (suppress storms). · Channel delivery failure isolation. · Concurrent samples for the same metric.

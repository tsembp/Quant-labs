# C++ Trading-Systems Learning Plan

## Goal

Use this repository to become comfortable building, testing, and measuring a
C++ trading-system component. The target is not to imitate a production HFT
firm; it is to develop the C++ and systems-engineering foundations needed to
reason about that kind of software.

## How we will work

You write the code. Before each small milestone, we will discuss the behaviour,
the C++ concepts involved, and a test plan. You will attempt the implementation
first; I will help explain compiler errors, review the design, and suggest the
next small step. Do not copy a solution before you understand the test it must
make pass.

## Phase 1 — C++ order-book correctness

Build the C++ `OrderBook` until it has the same observable behaviour as the
Python reference.

1. Read and understand the current resting-order implementation.
2. Match a crossing limit order against the best opposite price level.
3. Record trades and handle partial fills.
4. Let an unfilled remainder rest in the book.
5. Add cancellation by order ID.
6. Add decrease-only order modification.
7. Add market orders.
8. Add L2 depth and simple execution VWAP.

**Done when:** every feature has focused C++ tests, and equivalent Python and
C++ order sequences produce the same trades and final top-of-book state.

## Phase 2 — Replay and software design

Build a small executable that reads a deterministic sequence of order events
from a file and feeds them to the book.

- Define a simple CSV event format.
- Keep parsing, order-book logic, and output separate.
- Report trades, final depth, and basic statistics.
- Add invalid-input tests and useful error messages.

**Done when:** somebody else can build the project, replay a sample file, and
understand the result from the README.

## Phase 3 — Measure performance

First measure the simple, correct version. Then change only one variable at a
time and record the result.

- Generate a repeatable workload.
- Measure throughput and latency distribution.
- Profile CPU time and count allocations.
- Compare at least one data-structure or allocation improvement.
- Document the benchmark machine, workload, and results.

**Done when:** the repository contains numbers and an explanation of the
trade-offs—not just a claim that it is “low latency.”

## Phase 4 — Controlled systems features

Only after the single-threaded engine is correct and measured:

- simulate a UDP market-data feed;
- define message sequencing and gap detection;
- add a simple producer/consumer boundary;
- learn the concurrency model before attempting lock-free structures.

**Done when:** you can explain ownership, thread boundaries, failure cases, and
why the design is safe.

## What to learn alongside the project

- Modern C++: classes, references, RAII, `const`, templates, smart pointers,
  standard containers, and error handling.
- Core CS: complexity, cache locality, memory layout, operating-system basics,
  threads, and networking.
- Engineering habits: Git, CMake, unit tests, debugging, profiling, and clear
  documentation.

## Portfolio finish line

This becomes a strong first systems project when you can demonstrate:

1. a correct and thoroughly tested matching engine;
2. a replayable workload and clear program boundaries;
3. benchmark results and evidence-based optimisation;
4. a short design document explaining important trade-offs.

Then build a second, complementary project—such as a market-data replay and
backtesting engine or an exchange-gateway simulator—instead of another order
book.

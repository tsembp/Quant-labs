# C++ Order Book Lab

This is a gradual C++ rebuild of the [Python reference implementation](../python_labs/README.md).
It is intentionally built one tested capability at a time, so the focus stays
on how the same trading concepts map to C++ data structures and tests.

If you are new to intermediate C++, read [BEGINNER_NOTES.md](BEGINNER_NOTES.md)
before working through the implementation.

## Milestone 1: resting order storage

`OrderBook` currently stores valid resting limit orders and reports the best
bid and best ask. It uses:

- `std::map` for price priority: high-to-low for bids and low-to-high for asks.
- `std::deque` at each price level for FIFO/time priority.
- integer price ticks rather than floating-point prices, avoiding rounding
  errors. For example, with a $0.01 tick, `10'125` represents $101.25.

Matching, cancellation, and market orders are deliberately not implemented
yet. The next milestone is to match an incoming order against the best
opposite price level and emit a trade.

## Build and test

From the repository root:

```bash
cmake -S cpp_labs -B /tmp/quant-labs-cpp-build
cmake --build /tmp/quant-labs-cpp-build
ctest --test-dir /tmp/quant-labs-cpp-build --output-on-failure
```

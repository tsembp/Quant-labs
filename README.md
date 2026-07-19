# Quant Labs

An educational repository for building the core components of electronic
trading systems. It starts with a working Python reference implementation and
rebuilds the same ideas in C++ to learn the data structures, testing, and
performance trade-offs involved in an order book.

This is a learning project, not production trading software or financial
advice.

## What's here

| Lab | Status | Focus |
| --- | --- | --- |
| [Python](python_labs/README.md) | Reference implementation | Matching, order lifecycle, market data, and multi-venue routing |
| [C++](cpp_labs/README.md) | In progress | Rebuilding the order book incrementally with CMake and tests |

## Quick start

Run the Python reference tests:

```bash
python -m pip install -r python_labs/requirements.txt
python -m unittest discover -s python_labs/tests -v
```

Build and test the C++ lab:

```bash
cmake -S cpp_labs -B /tmp/quant-labs-cpp-build
cmake --build /tmp/quant-labs-cpp-build
ctest --test-dir /tmp/quant-labs-cpp-build --output-on-failure
```


## Repository layout

```text
python_labs/  Working Python reference implementation and tests
cpp_labs/     Incremental C++ implementation, CMake configuration, and tests
```

# Quant-Labs

Hands-on quantitative development projects for learning market microstructure and quantitative finance.


## Python-based Labs (`/python_labs`)

### `limit_order_book.py`

Single-venue limit order book with price–time priority.

**Features implemented:**
- Limit orders (buy/sell) with FIFO matching at each price
- Market orders that sweep the book and never rest
- Partial fills and automatic removal of filled orders
- Order cancellation by ID
- Order quantity modification (decrease-only)
- Best bid and best ask access
- Trade tape recording executed trades
- Deterministic ordering using timestamps

This file provides the base matching engine for future extensions such as depth aggregation, VWAP/VWMA analytics, and multi-venue routing.
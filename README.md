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
- L2 depth aggregation (price levels)
- Sweep VWAP calculation from current book
- VWMA (volume-weighted moving average) over last *N* trades
- Deterministic ordering using timestamps

---

### `multi_venue_book.py`

Multi-venue order book aggregation built on top of single-venue books.

**Features implemented:**
- Multiple exchange support (e.g. Binance, Crypto.com)
- Per-venue best bid / best ask
- Per-venue liquidity statistics
- NBBO (National Best Bid and Offer) across venues
- Smart order routing with cross-venue sweep VWAP
- Per-venue fill attribution
- Consolidated L2 depth across all venues

These components model realistic multi-exchange market data and routing behavior used in electronic trading systems. :contentReference[oaicite:0]{index=0}

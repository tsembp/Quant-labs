# Python Order Book Labs

The Python lab is the behavioural reference for this repository. It models a
single-exchange limit order book and builds a multi-venue aggregation layer on
top of it.

## Components

### `limit_order_book.py`

`OrderBook` implements price-time-priority matching:

- limit buy and sell orders, with FIFO execution at each price;
- market orders that sweep available liquidity and never rest;
- partial fills, cancellation by ID, and decrease-only quantity changes;
- best bid/ask and aggregated L2 price levels;
- a trade tape in `OrderBook.trades`;
- an append-only, structured activity log in `OrderBook.events`;
- sweep VWAP quotes and VWMA over the last *N* trades.

### `multi_venue_book.py`

`MultiVenueBook` combines several `OrderBook` instances to provide:

- per-venue top-of-book and liquidity statistics;
- NBBO (best bid and offer across all venues);
- consolidated L2 depth;
- smart-order-routing estimates, including cross-venue VWAP and fill
  attribution.

## Run the tests

From the repository root:

```bash
python -m pip install -r python_labs/requirements.txt
python -m unittest discover -s python_labs/tests -v
```

The tests cover price and time priority, partial fills, market sweeps, order
lifecycle actions, VWAP/VWMA, and cross-venue routing.

## Notes

The code represents prices and quantities as simple Python numbers to keep the
lab approachable. Production trading systems normally define explicit tick and
quantity types, avoid floating-point money values, add persistence and
recovery, and handle concurrency and exchange-specific rules.

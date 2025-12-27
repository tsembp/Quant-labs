from typing import Dict, Any, Optional, Tuple, List
from limit_order_book import OrderBook
from collections import defaultdict

class MultiVenueBook:
    def __init__(self):
        self.venues: Dict[str, OrderBook] = {}

    def add_venue(self, name: str, book: Optional[OrderBook] = None):
        if name in self.venues:
            raise ValueError(f"venue '{name}' already exists")
        self.venues[name] = book if book is not None else OrderBook()

    def get_venue(self, name: str) -> OrderBook:
        if name not in self.venues:
            raise KeyError(f"unknown venue '{name}'")
        return self.venues[name]

    def venue_top(self, name: str) -> Dict[str, Any]:
        ob = self.get_venue(name)
        bb = ob.best_bid()
        ba = ob.best_ask()
        return {
            "venue": name,
            "best_bid": None if bb is None else (bb.price, bb.qty),
            "best_ask": None if ba is None else (ba.price, ba.qty),
        }

    def venue_liquidity(self, name: str) -> Dict[str, Any]:
        ob = self.get_venue(name)
        bid_qty = sum(o.qty for o in ob.bids)
        ask_qty = sum(o.qty for o in ob.asks)
        return {
            "venue": name,
            "total_bid_qty": bid_qty,
            "total_ask_qty": ask_qty,
        }

    def venue_sweep_vwap(self, name: str, side: str, qty: float) -> Dict[str, Any]:
        ob = self.get_venue(name)
        out = ob.sweep_vwap(side, qty)
        out["venue"] = name
        return out

    def nbbo(self) -> Dict[str, Optional[Tuple[float, float, str]]]:
        """
        NBBO = National Best Bid and Offer = best bid across venues & best ask across venues.
        Returns tuples: (price, qty_at_that_top_order, venue)
        """
        best_bid = None  # (price, qty, venue)
        best_ask = None  # (price, qty, venue)

        for v, ob in self.venues.items():
            bb = ob.best_bid()
            ba = ob.best_ask()

            if bb is not None:
                cand = (bb.price, bb.qty, v)
                if best_bid is None or cand[0] > best_bid[0]:
                    best_bid = cand

            if ba is not None:
                cand = (ba.price, ba.qty, v)
                if best_ask is None or cand[0] < best_ask[0]:
                    best_ask = cand

        return {"best_bid": best_bid, "best_ask": best_ask}

    def smart_sweep_vwap(self, side: str, qty: float) -> Dict[str, Any]:
        """
        Fill qty across venues at best available prices.
        BUY: consumes asks across venues from lowest to highest price
        SELL: consumes bids across venues from highest to lowest price
        """
        if side not in ["buy", "sell"]:
            raise ValueError("side must be 'buy' or 'sell'")
        if qty <= 0:
            raise ValueError("qty must be > 0")

        ladder: List[Tuple[float, float, str]] = []  # (price, level_qty, venue)

        if side == "buy":
            # collect all asks levels from all venues
            for v, ob in self.venues.items():
                for price, level_qty in ob.levels("sell", depth=10**9):
                    ladder.append((price, level_qty, v))
            ladder.sort(key=lambda x: x[0])  # cheapest asks first
        else:
            # collect all bid levels from all venues
            for v, ob in self.venues.items():
                for price, level_qty in ob.levels("buy", depth=10**9):
                    ladder.append((price, level_qty, v))
            ladder.sort(key=lambda x: -x[0])  # highest bids first

        remaining = qty
        filled = 0.0
        notional = 0.0
        breakdown = []  # (venue, price, qty)

        for price, level_qty, venue in ladder:
            if remaining <= 0:
                break
            take = min(remaining, level_qty)
            notional += take * price
            filled += take
            remaining -= take
            breakdown.append({"venue": venue, "price": price, "qty": take})

        vwap = (notional / filled) if filled > 0 else None

        # Per-venue totals (nice for the interview follow-up)
        per_venue = {}
        for b in breakdown:
            v = b["venue"]
            per_venue.setdefault(v, {"filled_qty": 0.0, "notional": 0.0})
            per_venue[v]["filled_qty"] += b["qty"]
            per_venue[v]["notional"] += b["qty"] * b["price"]

        return {
            "side": side,
            "requested_qty": qty,
            "filled_qty": filled,
            "remaining_qty": remaining,
            "notional": notional,
            "vwap": vwap,
            "breakdown": breakdown,
            "per_venue": per_venue,
        }

    def consolidated_levels(self, side: str, depth: int = 10):
        """
        Consolidated (cross-venue) L2 depth.
        Merges all venues levels by price: (price -> total_qty).
        side='buy' returns bids high->low, side='sell' returns asks low->high.
        """
        if side not in ["buy", "sell"]:
            raise ValueError("side must be 'buy' or 'sell'")
        if depth <= 0:
            raise ValueError("depth must be > 0")

        agg = defaultdict(float)

        # Merge venue levels into one price->qty map
        for venue, ob in self.venues.items():
            for price, qty in ob.levels(side, depth=10**9):
                agg[price] += qty

        # Sort prices like a real book
        prices = sorted(agg.keys(), reverse=(side == "buy"))
        return [(p, agg[p]) for p in prices[:depth]]

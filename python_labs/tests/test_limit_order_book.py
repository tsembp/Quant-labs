import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from limit_order_book import OrderBook


class OrderBookTest(unittest.TestCase):
    def test_price_time_priority_at_same_price(self):
        book = OrderBook()
        first = book.add_order('sell', 101, 2)
        second = book.add_order('sell', 101, 2)

        book.add_order('buy', 101, 3)

        self.assertEqual(
            book.trades,
            [
                {'buyer': 'o3', 'seller': first, 'price': 101, 'qty': 2},
                {'buyer': 'o3', 'seller': second, 'price': 101, 'qty': 1},
            ],
        )
        self.assertEqual(book.best_ask().order_id, second)
        self.assertEqual(book.best_ask().qty, 1)

    def test_best_price_has_priority_over_earlier_worse_price(self):
        book = OrderBook()
        book.add_order('sell', 102, 1)
        cheaper = book.add_order('sell', 101, 1)

        book.add_order('buy', 102, 1)

        self.assertEqual(book.trades[0]['seller'], cheaper)
        self.assertEqual(book.best_ask().price, 102)

    def test_partial_limit_fill_rests_the_remainder(self):
        book = OrderBook()
        book.add_order('sell', 100, 2)
        order_id = book.add_order('buy', 101, 5)

        self.assertEqual(book.order_map[order_id].qty, 3)
        self.assertEqual(book.best_bid().price, 101)
        self.assertEqual(book.trades[0]['qty'], 2)

    def test_market_order_sweeps_and_never_rests(self):
        book = OrderBook()
        book.add_order('sell', 100, 2)
        book.add_order('sell', 101, 2)

        result = book.add_market_order('buy', 5)

        self.assertEqual(result['filled_qty'], 4)
        self.assertEqual(result['remaining_qty'], 1)
        self.assertFalse(any(order.order_id == result['order_id'] for order in book.bids))
        self.assertIsNone(book.best_ask())

    def test_cancel_and_decrease_only_modify(self):
        book = OrderBook()
        order_id = book.add_order('buy', 99, 5)

        self.assertTrue(book.modify_order_qty(order_id, 3))
        self.assertEqual(book.order_map[order_id].qty, 3)
        self.assertFalse(book.modify_order_qty(order_id, 4))
        self.assertTrue(book.cancel_order(order_id))
        self.assertFalse(book.cancel_order(order_id))
        self.assertIsNone(book.best_bid())

    def test_depth_vwap_and_trade_vwma(self):
        book = OrderBook()
        book.add_order('sell', 100, 2)
        book.add_order('sell', 102, 3)

        self.assertEqual(book.levels('sell'), [(100, 2.0), (102, 3.0)])
        quote = book.sweep_vwap('buy', 4)
        self.assertEqual(quote['filled_qty'], 4.0)
        self.assertEqual(quote['vwap'], 101.0)

        book.add_market_order('buy', 4)
        self.assertEqual(book.vwma_last_n_trades(2), 101.0)

    def test_invalid_inputs_are_rejected(self):
        book = OrderBook()
        with self.assertRaises(ValueError):
            book.add_order('hold', 100, 1)
        with self.assertRaises(ValueError):
            book.add_order('buy', 0, 1)
        with self.assertRaises(ValueError):
            book.add_market_order('buy', 0)


if __name__ == '__main__':
    unittest.main()

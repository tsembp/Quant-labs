import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from multi_venue_book import MultiVenueBook


class MultiVenueBookTest(unittest.TestCase):
    def test_nbbo_consolidated_depth_and_smart_routing(self):
        book = MultiVenueBook()
        book.add_venue('alpha')
        book.add_venue('beta')
        book.get_venue('alpha').add_order('sell', 101, 2)
        book.get_venue('alpha').add_order('buy', 99, 4)
        book.get_venue('beta').add_order('sell', 100, 3)
        book.get_venue('beta').add_order('buy', 98, 1)

        self.assertEqual(book.nbbo()['best_ask'], (100, 3, 'beta'))
        self.assertEqual(book.nbbo()['best_bid'], (99, 4, 'alpha'))
        self.assertEqual(book.consolidated_levels('sell'), [(100, 3.0), (101, 2.0)])

        quote = book.smart_sweep_vwap('buy', 4)
        self.assertEqual(quote['vwap'], 100.25)
        self.assertEqual(quote['per_venue']['beta']['filled_qty'], 3.0)
        self.assertEqual(quote['per_venue']['alpha']['filled_qty'], 1.0)


if __name__ == '__main__':
    unittest.main()

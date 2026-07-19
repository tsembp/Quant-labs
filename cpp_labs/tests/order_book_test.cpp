#include "order_book.hpp"

#include <cassert>
#include <iostream>
#include <stdexcept>

using quant_labs::OrderBook;
using quant_labs::Side;

int main() {
    OrderBook book;

    // The map comparator puts the highest bid at begin().
    book.add_limit_order(Side::Buy, 10'000, 2);
    book.add_limit_order(Side::Buy, 10'100, 3);
    book.add_limit_order(Side::Buy, 10'100, 4);

    const auto bid = book.best_bid();
    assert(bid.has_value());
    assert(bid->price == 10'100);
    assert(bid->quantity == 7);  // Both orders at the best price are aggregated.

    book.add_limit_order(Side::Sell, 10'300, 5);
    book.add_limit_order(Side::Sell, 10'200, 1);

    const auto ask = book.best_ask();
    assert(ask.has_value());
    assert(ask->price == 10'200);
    assert(ask->quantity == 1);
    assert(book.order_count() == 5);

    bool rejected_invalid_order = false;
    try {
        book.add_limit_order(Side::Buy, 0, 1);
    } catch (const std::invalid_argument&) {
        rejected_invalid_order = true;
    }
    assert(rejected_invalid_order);

    std::cout << "order_book_tests: passed\n";
}

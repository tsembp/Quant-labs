#include "order_book.hpp"

#include <stdexcept>

namespace quant_labs {

OrderId OrderBook::add_limit_order(Side side, Price price, Quantity quantity) {
    if (price <= 0) {
        throw std::invalid_argument("price must be positive");
    }
    if (quantity <= 0) {
        throw std::invalid_argument("quantity must be positive");
    }

    const Order order{next_order_id_++, side, price, quantity};

    // operator[] finds the price level or creates an empty one; push_back gives
    // orders at the same price first-in, first-out priority.
    if (side == Side::Buy) {
        bids_[price].push_back(order);
    } else {
        asks_[price].push_back(order);
    }

    return order.id;
}

std::optional<Quote> OrderBook::best_bid() const {
    if (bids_.empty()) {
        return std::nullopt;
    }
    const auto& [price, level] = *bids_.begin();
    return Quote{price, level_quantity(level)};
}

std::optional<Quote> OrderBook::best_ask() const {
    if (asks_.empty()) {
        return std::nullopt;
    }
    const auto& [price, level] = *asks_.begin();
    return Quote{price, level_quantity(level)};
}

std::size_t OrderBook::order_count() const {
    std::size_t count = 0;
    for (const auto& [price, level] : bids_) {
        (void)price;
        count += level.size();
    }
    for (const auto& [price, level] : asks_) {
        (void)price;
        count += level.size();
    }
    return count;
}

Quantity OrderBook::level_quantity(const PriceLevel& level) {
    Quantity total = 0;
    for (const Order& order : level) {
        total += order.quantity;
    }
    return total;
}

}  // namespace quant_labs

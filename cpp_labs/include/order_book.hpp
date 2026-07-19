#pragma once

#include <cstdint>
#include <deque>
#include <map>
#include <optional>
#include <string>

namespace quant_labs {

using OrderId = std::uint64_t;
using Price = std::int64_t;  // Price in the smallest tick, e.g. 10'125 = $101.25.
using Quantity = std::int64_t;

enum class Side { Buy, Sell };

struct Order {
    OrderId id;
    Side side;
    Price price;
    Quantity quantity;
};

struct Quote {
    Price price;
    Quantity quantity;
};

class OrderBook {
public:
    // Milestone 1: store a resting order. Matching comes in the next step.
    OrderId add_limit_order(Side side, Price price, Quantity quantity);

    [[nodiscard]] std::optional<Quote> best_bid() const;
    [[nodiscard]] std::optional<Quote> best_ask() const;
    [[nodiscard]] std::size_t order_count() const;

private:
    using PriceLevel = std::deque<Order>;
    using Bids = std::map<Price, PriceLevel, std::greater<Price>>;
    using Asks = std::map<Price, PriceLevel, std::less<Price>>;

    static Quantity level_quantity(const PriceLevel& level);

    Bids bids_;
    Asks asks_;
    OrderId next_order_id_ = 1;
};

}  // namespace quant_labs

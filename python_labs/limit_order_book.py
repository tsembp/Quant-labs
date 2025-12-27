from sortedcontainers import SortedList

class Order:
    def __init__(self, order_id, side, price, qty, timestamp):
        self.order_id = order_id
        self.side = side    # buy or sell
        self.price = price
        self.qty = qty
        self.timestamp = timestamp

    def __repr__(self):
        return f"Order(id={self.order_id}, side={self.side}, price={self.price}, qty={self.qty}, ts={self.timestamp})"

class OrderBook:
    def __init__(self):
        self.bids = SortedList(key=lambda o: (-o.price, o.timestamp)) # desc price, FIFO timestamp
        self.asks = SortedList(key=lambda o: (o.price, o.timestamp)) # asc price, FIFO timestamp
        self.order_map = {}
        self.timestamp = 0
        self.trades = []
        
    def add_order(self, side, price, qty=1):
        if side not in ['buy', 'sell']:
            raise ValueError("side must be 'buy' or 'sell'")
        
        self.timestamp += 1
        order_id = f"o{self.timestamp}"
        incoming = Order(order_id, side, price, qty, self.timestamp)

        if side == 'buy':
            # match against asks where:
            #   - we have qty
            #   - ask price <= bid price
            while incoming.qty > 0:
                best_ask = self.best_ask()
                if best_ask is None or best_ask.price > incoming.price:
                    print('No matching asks')
                    break
                
                trade_qty = min(incoming.qty, best_ask.qty)
                trade_price = best_ask.price

                self.trades.append({
                    'buyer' : incoming.order_id,
                    'seller' : best_ask.order_id,
                    'price' : trade_price,
                    'qty' : trade_qty
                })

                print(f"Trade executed: {trade_qty} @ {trade_price} between {incoming.order_id} and {best_ask.order_id}")

                # update qtys
                incoming.qty -= trade_qty
                best_ask.qty -= trade_qty

                if best_ask.qty == 0:
                    self.asks.remove(best_ask)
                    del self.order_map[best_ask.order_id]
            
            if incoming.qty > 0:
                self.bids.add(incoming)
                self.order_map[incoming.order_id] = incoming
        
        elif side == 'sell':
            # match against bids where:
            #   - we have qty
            #   - bid price >= ask price
            while incoming.qty > 0:
                best_bid = self.best_bid()
                if best_bid is None or best_bid.price < incoming.price:
                    print('No matching bids')
                    break
                
                trade_qty = min(incoming.qty, best_bid.qty)
                trade_price = best_bid.price

                self.trades.append({
                    'buyer' : best_bid.order_id,
                    'seller' : incoming.order_id,
                    'price' : trade_price,
                    'qty' : trade_qty
                })

                print(f"Trade executed: {trade_qty} @ {trade_price} between {best_bid.order_id} and {incoming.order_id}")

                # update qtys
                incoming.qty -= trade_qty
                best_bid.qty -= trade_qty

                if best_bid.qty == 0:
                    self.bids.remove(best_bid)
                    del self.order_map[best_bid.order_id]
            
            if incoming.qty > 0:
                self.asks.add(incoming)
                self.order_map[incoming.order_id] = incoming

        return incoming.order_id
    
    def add_market_order(self, side, qty=1):
        """
        Add MARKET order.
        - Never rests in the book.
        - Trades against best prices until qty is exhausted or opposite book is empty.
        """
        if side not in ['buy', 'sell']:
            raise ValueError("side must be 'buy' or 'sell'")
        
        self.timestamp += 1
        order_id = f"o{self.timestamp}"
        remaining_qty = qty
        filled = 0

        if side == 'buy':
            while remaining_qty > 0: # repeatedly hits best ask
                best_ask = self.best_ask()
                if best_ask is None:
                    print('No matching asks for market buy order')
                    break
                
                trade_qty = min(remaining_qty, best_ask.qty)
                trade_price = best_ask.price

                self.trades.append({
                    'buyer' : order_id,
                    'seller' : best_ask.order_id,
                    'price' : trade_price,
                    'qty' : trade_qty
                })

                print(f"Market Buy Trade executed: {trade_qty} @ {trade_price} between {order_id} and {best_ask.order_id}")

                remaining_qty -= trade_qty
                filled += trade_qty
                best_ask.qty -= trade_qty

                if best_ask.qty == 0:
                    self.asks.remove(best_ask)
                    del self.order_map[best_ask.order_id]
        elif side == 'sell':
            while remaining_qty > 0: # repeatedly hits best bid
                best_bid = self.best_bid()
                if best_bid is None:
                    print('No matching bids for market sell order')
                    break
                
                trade_qty = min(remaining_qty, best_bid.qty)
                trade_price = best_bid.price

                self.trades.append({
                    'buyer' : best_bid.order_id,
                    'seller' : order_id,
                    'price' : trade_price,
                    'qty' : trade_qty
                })

                print(f"Market Sell Trade executed: {trade_qty} @ {trade_price} between {best_bid.order_id} and {order_id}")

                remaining_qty -= trade_qty
                filled += trade_qty
                best_bid.qty -= trade_qty

                if best_bid.qty == 0:
                    self.bids.remove(best_bid)
                    del self.order_map[best_bid.order_id]

        return {
            'order_id' : order_id,
            'side' : side,
            'requested_qty' : qty,
            'filled_qty' : filled,
            'remaining_qty' : remaining_qty
        }
        
    def modify_order_qty(self, order_id, new_qty):
        if order_id not in self.order_map:
            print(f"modify_order_qty: Order ID {order_id} not found")
            return False
        
        order = self.order_map[order_id]
        if new_qty <= 0:
            print(f"modify_order_qty: New quantity must be positive")
            return False
        
        if new_qty > order.qty:
            print(f"modify_order_qty: cannot increase qty from {order.qty} to {new_qty} for order {order_id}")
            return False
        
        order.qty = new_qty
        print(f"modify_order_qty: Order {order_id} qty modified to {new_qty}")
        return True

    def cancel_order(self, order_id):
        if order_id in self.order_map:
            order = self.order_map[order_id]
            if order.side == 'buy':
                print(f"cancel_order: Cancelling buy order {order_id}")
                self.bids.remove(order)
            elif order.side == 'sell':
                print(f"cancel_order: Cancelling sell order {order_id}")
                self.asks.remove(order)
            del self.order_map[order_id]
            return True
        
        print(f"cancel_order: Order ID {order_id} not found")
        return False
    
    def best_bid(self): # max
        if not self.bids:
            return None
        return self.bids[0]
    
    def best_ask(self): # min
        if not self.asks:
            return None
        return self.asks[0]
    
    def print_book(self):
        print("Order Book:")
        print("Bids:")
        for bid in self.bids:
            print(f"  {bid}")
        print("Asks:")
        for ask in self.asks:
            print(f"  {ask}")
        print("")

if __name__ == "__main__":
    ob = OrderBook()
    id1 = ob.add_order('buy', price=100, qty=10)
    id2 = ob.add_order('buy', price=100, qty=5)
    ob.print_book()

    # Reduce first order from 10 -> 6
    ob.modify_order_qty(id1, 6)
    ob.print_book()

    # Try to increase (should fail)
    ob.modify_order_qty(id1, 20)

    # Reduce to zero (should cancel)
    ob.modify_order_qty(id2, 0)
    ob.print_book()

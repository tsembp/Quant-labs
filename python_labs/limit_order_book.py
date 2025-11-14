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
    
    def cancel_order(self, order_id):
        if order_id in self.order_map:
            order = self.order_map[order_id]
            if order.side == 'buy':
                self.bids.remove(order)
            elif order.side == 'sell':
                self.asks.remove(order)
            del self.order_map[order_id]
            return True
        return False
    
    def best_bid(self): # max
        if not self.bids:
            return None
        return self.bids[0]
    
    def best_ask(self): # min
        if not self.asks:
            return None
        return self.asks[0]
    
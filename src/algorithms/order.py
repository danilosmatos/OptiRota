from collections import deque

class OrderQueue:
    def __init__(self):
        self.queue = deque() 

    def enqueue_order(self, order_id, coords, demand, time_window):
        order = {
            'id': order_id, 
            'coords': coords, 
            'demand': demand, 
            'time_window': time_window
        }
        self.queue.append(order)

    def process_all_orders(self):
        return [self.queue.popleft() for _ in range(len(self.queue))]
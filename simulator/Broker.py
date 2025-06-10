from random import random

from Bot import Bot
import random

class Broker:
    def __init__(self, broker_id):
        self.broker_id = broker_id
        self.subscribers = []  
        self.publishers = []  
        self.elected_publisher = None  
        self.publishers.append(Bot(0, False))
        self.last_iteration_number=-1 
        self.hops_to_cc = float('inf') 

    def add_subscriber(self, bot):
        self.subscribers.append(bot)

    def add_publisher(self, bot):
        self.publishers.append(bot)

    def shuffle_publishers(self):
        random.shuffle(self.publishers)

    def elect_publisher(self,iteration_number):
        assert len(self.publishers) >= 1
        assert (len(self.publishers)==1 and self.publishers[0].bot_id == 0) or len(self.publishers) > 1
        if iteration_number<len(self.publishers):
            self.elected_publisher = self.publishers[iteration_number]
            self.last_iteration_number=iteration_number
            return True
        return False



class Bot:
    def __init__(self, bot_id, is_relay):
        self.bot_id = bot_id
        self.is_relay = is_relay
        self.broker = None 
        self.publish_brokers = [] 
        self.connected_to_cc = False  
        self.hops_to_cc = float('inf')  

    def assign_broker(self, broker):
        self.broker = broker

    def set_publish_brokers(self, publish_brokers):
        self.publish_brokers = publish_brokers

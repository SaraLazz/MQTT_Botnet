import random
import numpy as np

from Bot import Bot
from Broker import Broker


class Network:
    def __init__(self, num_brokers, num_bots, prob_relay, num_brokers_per_relay):
        self.brokers = [Broker(f"broker_{i}") for i in range(num_brokers)]
        self.bots = [
            Bot(f"bot_{i}", (random.random() * 100) < prob_relay)
            for i in range(1,num_bots)
        ]
        self.num_brokers_per_relay = num_brokers_per_relay
        self.max_retries = 0 


    def initialize(self):
        print("START inizialize")
        for bot in self.bots:
            assigned_broker = random.choice(self.brokers)
            bot.assign_broker(assigned_broker)
            assigned_broker.add_subscriber(bot) 
            if bot.is_relay:
                publish_brokers = random.sample(self.brokers, k=self.num_brokers_per_relay) 
                if assigned_broker in publish_brokers: 
                    publish_brokers.remove(assigned_broker)
                bot.set_publish_brokers(publish_brokers)
                for broker in publish_brokers:
                    broker.add_publisher(bot)
        for broker in self.brokers:
            broker.shuffle_publishers()
        print("END inizialize")

    
    def propagate_commands(self):
        num_iteration=0
        connected_bots = set()
        brokers_to_adjust = self.brokers.copy()
        while True:
            for broker in brokers_to_adjust: 
                res=broker.elect_publisher(num_iteration)
                assert res

            for broker in self.brokers:
                if broker not in brokers_to_adjust:
                    continue
                traversed_pub=set()
                current_broker = broker
                current_pub = current_broker.elected_publisher
                #print(broker.publishers)
                hops_to_cc = 0
                len_checked=0
                while True:
                    len_checked+=1
                    if current_pub in traversed_pub and current_pub.bot_id != 0:
                        break
                    traversed_pub.add(current_pub)
                    if current_pub.bot_id == 0:
                        brokers_to_adjust.remove(broker)
                        broker.hops_to_cc = hops_to_cc + 1
                        for bot in broker.subscribers:
                            bot.connected_to_cc = True
                            bot.hops_to_cc = hops_to_cc + 1
                            connected_bots.add(bot)
                        break
                    else:
                        current_broker = current_pub.broker
                        current_pub = current_broker.elected_publisher
                        hops_to_cc = hops_to_cc + 1
            if len(connected_bots)==len(self.bots):
                print(f"the connected bots are {len(connected_bots)} at iteration number {num_iteration}")
                break
            else:
                print(f"the connected bots are {len(connected_bots)} at iteration number {num_iteration}")
                num_iteration += 1

        self.max_retries = num_iteration


    def min_set_cover(self, remaining=False):
        all_publishers = set()
        for b in self.brokers:
            selected_publishers = b.publishers[b.last_iteration_number:] if remaining else b.publishers
            all_publishers.update({bt.bot_id for bt in selected_publishers})

        U = all_publishers - {0}  # Escludiamo il C&C

        complements = {
            b: U - {bt.bot_id for bt in (b.publishers[b.last_iteration_number:] if remaining else b.publishers)}
            for b in self.brokers
        }

        covered = set()
        selected_brokers = []

        while covered != U:
            best_broker = max(complements, key=lambda b: len(complements[b] - covered))
            selected_brokers.append(best_broker)
            covered.update(complements[best_broker])
            del complements[best_broker]  # Rimuoviamo il broker selezionato

        assert set.intersection(
            *[{bt.bot_id for bt in (b.publishers[b.last_iteration_number:] if remaining else b.publishers)} for b in
              selected_brokers]
        ) == {0}

        return selected_brokers

    def random_broker_selection(self, remaining=False):
        random.shuffle(self.brokers) 
        selected_brokers = []

        first_broker_publishers = {bt.bot_id for bt in (
            self.brokers[0].publishers[self.brokers[0].last_iteration_number:] if remaining else self.brokers[
                0].publishers)}
        intersection_set = first_broker_publishers.copy()

        selected_brokers.append(self.brokers[0])

        if intersection_set == {0}: 
            return selected_brokers

        for broker in self.brokers[1:]:
            selected_brokers.append(broker)
            broker_publishers = {bt.bot_id for bt in
                                 (broker.publishers[broker.last_iteration_number:] if remaining else broker.publishers)}
            intersection_set.intersection_update(broker_publishers)

            if intersection_set == {0}:
                return selected_brokers

        return selected_brokers


    def run(self):
        self.initialize()
        self.propagate_commands() 

        min_set_collaborating_brokers=self.min_set_cover(remaining=False)
        random_set_collaborating_brokers=self.random_broker_selection(remaining=False)
        min_set_collaborating_brokers_remaining=self.min_set_cover(remaining=True)
        random_set_collaborating_brokers_remaining=self.random_broker_selection(remaining=True)

        number_hops_to_CC_list = [b.hops_to_cc for b in self.brokers]
        median_number_hops_to_CC_list = sum(number_hops_to_CC_list) / len(number_hops_to_CC_list)
        std_number_hops_to_CC_list = np.std(number_hops_to_CC_list)

        number_attempts_to_regime_list = [b.last_iteration_number+1 for b in self.brokers]
        median_attempts_to_regime_list = sum(number_attempts_to_regime_list) / len(number_attempts_to_regime_list)
        std_attempts_to_regime_list = np.std(number_attempts_to_regime_list)

        number_relay_list = [len(b.publishers) for b in self.brokers]
        median_relay_list = sum(number_relay_list) / len(number_relay_list)
        std_relay_list = np.std(number_relay_list)
        #print(f"Number relay list: {number_relay_list}")
        #print(f"number of iteration list: {[b.last_iteration_number for b in self.brokers]}")
        #print(f"Elected publisher list: {[b.elected_publisher.bot_id for b in self.brokers]}")

        number_remaining_relay_list = [(len(b.publishers) - b.last_iteration_number - 1) for b in self.brokers]
        median_remaining_relay_list = sum(number_remaining_relay_list) / len(number_remaining_relay_list)
        std_remaining_relay_list = np.std(number_remaining_relay_list)
        #print(f"Remaining relay list: {number_remaining_relay_list}")

        cc_publish_brokers = sum(1 for broker in self.brokers if broker.elected_publisher.bot_id == 0)

        relay_bots=[bt.bot_id for bt in self.bots if bt.is_relay]
        bots_publisher_connections={bt:0 for bt in relay_bots}
        for b in self.brokers:
            if b.elected_publisher.bot_id == 0:
                continue
            bots_publisher_connections[b.elected_publisher.bot_id]=bots_publisher_connections[b.elected_publisher.bot_id]+1
        #connections = list(bots_publisher_connections.values())
        connections = [conn for conn in bots_publisher_connections.values() if conn != 0]
        #print(f"num of actual publishers {len(connections)}")
        median_connections = sum(connections) / len(connections)
        std_connections = np.std(connections)

        brokers_zero_relays = sum(1 for b in self.brokers if len(b.publishers) == 1)

        brokers_zero_remaining_relays = sum(1 for b in self.brokers if (len(b.publishers) - b.last_iteration_number - 1) == 0) 


        return {
            "total retries": self.max_retries + 1,
            "cc_publish_brokers": cc_publish_brokers,
            "median hops to CC": median_number_hops_to_CC_list,
            "std hops to CC": std_number_hops_to_CC_list,
            "median attempts to regime": median_attempts_to_regime_list,
            "std attempts to regime": std_attempts_to_regime_list,
            "median number of remaining relay in brokers": median_remaining_relay_list,
            "std number of remaining relay in brokers": std_remaining_relay_list,
            "median relay per broker": median_relay_list,
            "std relay per broker": std_relay_list,
            "brokers not conceiling the C&C": brokers_zero_relays,
            "brokers not conceiling the REMANINING C&C": brokers_zero_remaining_relays,
            "number of minimum required collaborating brokers": len(min_set_collaborating_brokers),
            "number of randomly selected required collaborating brokers": len(random_set_collaborating_brokers),
            "number of minimum required collaborating brokers (REMAINING)": len(min_set_collaborating_brokers_remaining),
            "number of randomly selected required collaborating brokers (REMAINING)": len(random_set_collaborating_brokers_remaining),
            "median connections of relay":median_connections,
            "std connections of relay":std_connections
        }
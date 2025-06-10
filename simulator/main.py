import math
import sys

from Network import Network

#if __name__ == "__main__":
def simulation(num_bots, prob_relay, num_brokers, percentage_num_brokers_per_relay):

    print("#############PARAMS")
    print(f"prob_relay={prob_relay}")
    print(f"num_brokers={num_brokers}")
    print(f"percentage_num_brokers_per_relay={percentage_num_brokers_per_relay}")
    print("#############")

    num_brokers_per_relay = math.ceil(percentage_num_brokers_per_relay * num_brokers / 100)
    network = Network(num_brokers, num_bots, prob_relay, num_brokers_per_relay)
    results = network.run()

    print("Simulation Results:")
    print(f"Brokers with C&C as publisher: {results['cc_publish_brokers']}")
    assert results['cc_publish_brokers'] >= 1
    

    #NUMBER OF CONNECTION PER PUBLISHER (avg and std)
    print("#################NUMBER OF CONNECTION PER PUBLISHER (avg and std)")
    print(f"Average number of connections for relay bots: {results['median connections of relay']:.2f} and STD number of connections for relay bots: {results['std connections of relay']:.2f}")
    print("########################################################################")

    #CONCERNING SETUP COMPLEXITY
    print("#################CONCERNING SETUP COMPLEXITY")
    print(f"Total retries to reach regime: {results['total retries']}")
    print(f"Average attempts to regime: {results['median attempts to regime']:.2f} and STD attempts to regime: {results['std attempts to regime']:.2f}")
    assert results['median attempts to regime'] <= results['total retries']
    print("########################################################################")


    #CONCERNING THE PATH LENGHT
    print("#################CONCERNING THE PATH LENGHT")
    print(f"Average hops to C&C: {results['median hops to CC']:.2f} and STD hops to C&C: {results['std hops to CC']:.2f}")
    print("########################################################################")

    #CONCERNING RESISTANCE AGAINST TAKEDOWN ATTEMPTS
    print("#################CONCERNING RESISTANCE AGAINST TAKEDOWN ATTEMPTS")
    print(f"Average number of relay per broker: {results['median relay per broker']:.2f} and STD number of relay per broker: {results['std relay per broker']:.2f}")
    print(f"Average number of remaining relays per brokers: {results['median number of remaining relay in brokers']:.2f} and STD number of remaining relays per brokers: {results['std number of remaining relay in brokers']:.2f}")
    assert results['median relay per broker'] <= num_bots
    assert results['median number of remaining relay in brokers'] <= num_bots

    print(f"Brokers where C&C is the only publisher: {results['brokers not conceiling the C&C']}")
    print(f"Brokers where C&C is the only REMAINING publisher: {results['brokers not conceiling the REMANINING C&C']}")
    assert results['brokers not conceiling the C&C'] <= num_brokers
    assert results['brokers not conceiling the REMANINING C&C'] <= num_brokers

    print(f"Number of minimum required collaborating brokers: {results['number of minimum required collaborating brokers']}")
    print(f"Number of randomly selected required collaborating brokers: {results['number of randomly selected required collaborating brokers']}")
    assert results['number of minimum required collaborating brokers'] <= num_brokers
    assert results['number of randomly selected required collaborating brokers'] <= num_brokers

    print(f"Number of minimum required collaborating brokers (REMAINING): {results['number of minimum required collaborating brokers (REMAINING)']}")
    print(f"Number of randomly selected required collaborating brokers (REMAINING): {results['number of randomly selected required collaborating brokers (REMAINING)']}")
    assert results['number of minimum required collaborating brokers (REMAINING)'] <= num_brokers
    assert results['number of randomly selected required collaborating brokers (REMAINING)'] <= num_brokers
    print("########################################################################")

    return results





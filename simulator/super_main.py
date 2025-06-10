import os
import sys

import pandas as pd

from main import simulation

NUM_RUNS = 100
EXPERIMENT_DIR = "../BOTNET_EXPERIMENT"

num_bots = 100000
prob_relay_values = [0.05, 0.07, 0.1, 0.3, 0.5, 0.7, 1, 1.3, 1.5, 1.7, 2]
num_brokers_values = [100]
percentage_brokers_per_relay_values = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

os.makedirs(EXPERIMENT_DIR, exist_ok=True)


for prob_relay in prob_relay_values:
    for num_brokers in num_brokers_values:
        for percentage_brokers_per_relay in percentage_brokers_per_relay_values:

            config_name = f"prob{prob_relay}_brokers{num_brokers}_perc{percentage_brokers_per_relay}"
            config_path = os.path.join(EXPERIMENT_DIR, config_name)
            os.makedirs(config_path, exist_ok=True)

            print(f"Running experiment: {config_name}")

            data = []

            for run in range(NUM_RUNS):
                print(f"Run {run + 1}/{NUM_RUNS}...")
                simulation_result = {
                    "prob_relay": prob_relay,
                    "num_brokers": num_brokers,
                    "percentage_brokers_per_relay": percentage_brokers_per_relay,
                    "run": run + 1
                }

                res_dict = simulation(num_bots, prob_relay, num_brokers, percentage_brokers_per_relay)
                if res_dict == None:
                    print("FATAL ERROR")
                    sys.exit(0)
                simulation_result.update(res_dict)

                data.append(simulation_result)

            df = pd.DataFrame(data)
            csv_file = os.path.join(config_path, "results.csv")
            df.to_csv(csv_file,float_format='%.2f', index=False)

            print(f"  Results saved in {csv_file}\n")

print("All experiments completed successfully!")

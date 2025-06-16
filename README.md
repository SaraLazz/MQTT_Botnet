# MQTT_Botnet

This repository contains the Python-based simulator developed to validate the architecture of an MQTT-based botnet, as described in our research paper.

The simulation reproduces the dynamic construction of the botnet, including the role of relay bots and broker selection. It also models the communication paths until the system reaches a **steady state**, defined as the condition where all bots are successfully receiving commands from the Command-and-Control (C&C) server.

## Features

- Simulates large-scale botnet formation over MQTT brokers
- Models both direct and relay-based communication paths
- Computes metrics related to connectivity and takedown resistance
- Supports parameterized experimental campaigns over multiple configurations

## How to Run the Simulation

To execute the simulator, navigate to the `simulator/` directory and run:

```bash
python3 super_main.py
```

This will launch the simulation across different scenarios defined in the configuration section of the script.

##  Simulation Parameters

The following parameters can be configured directly in the super_main.py script. The values below correspond to those used in our paper:

| Parameter                             | Description                                            | Value                                                   |
| ------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------- |
| `NUM_RUNS`                            | Number of simulation runs per scenario                 | `100`                                                   |
| `EXPERIMENT_DIR`                      | Directory where results are stored                     | `"../BOTNET_EXPERIMENT"`                                |
| `num_bots`                            | Total number of bots in the simulation                 | `100000`                                                |
| `prob_relay_values`                   | List of values for the relay bot selection probability | `[0.05, 0.07, 0.1, 0.3, 0.5, 0.7, 1, 1.3, 1.5, 1.7, 2]` |
| `num_brokers_values`                  | Number of MQTT brokers used in the simulation          | `[100]`                                                 |
| `percentage_brokers_per_relay_values` | % of brokers each relay connects to                    | `[50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]`         |

Each combination of these parameters defines a distinct simulation scenario.

##  Output

Simulation results are stored in the `BOTNET_EXPERIMENT/` directory.

Each scenario produces a `results.csv` file summarizing the outcomes across `NUM_RUNS` runs.

The CSV files contain various performance and resilience metrics, described below.







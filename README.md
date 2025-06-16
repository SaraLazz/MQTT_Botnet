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

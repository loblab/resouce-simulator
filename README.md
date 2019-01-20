# Resouce Simulator

Simulate the interaction of resources with conflict

- Platform: Python 3.x, InfluxDB, Grafana
- Ver: 0.1
- Updated: 1/20/2019
- Created: 1/5/2019
- Author: loblab

![Screenshot](https://raw.githubusercontent.com/loblab/resource-simulator/master/screenshot.png)

## Workflow

- The framework provides "bus & clock" support
- Each model output a value in every cycle
- Write the values to InfluxDB
- Plots in Grafana. Since Grafana can auto refresh every 5 seconds, it looks like a slow but live simulation.


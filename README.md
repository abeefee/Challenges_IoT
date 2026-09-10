# Challenges and Homework - IoT Project 2025/26

*Puoi anche leggerlo in [Italiano](README.it.md)*

> **Academic Note:** This challenges were developed for the *Internet of Things* course at Politecnico di Milano (Academic Year 2025/26), achieving a final grade of **28/28**.

## Challenge 1 - Wokwi and Power Consumption

### Project Description
Development of a commercial-style IoT motion sensor for smart homes using Wokwi emulation. The device detects human motion and measures ambient illuminance, transmitting structured strings (MOTION_DETECTED-LUMINOSITY:ZZZ) via ESP-NOW to a central sink node. To optimize power usage, the node alternates between active sensing/transmission phases and deep sleep intervals.

### Technical Details
Implemented using an ESP32 microcontroller with an event-driven architecture. The deep sleep duration $X\text{ [s]}$ and battery energy $Y\text{ [J]}$ are dynamically parameterized based on the team leader's person code ($X = (AB \pmod{50} + 5) / 10$, $Y = (ABCD \pmod{5000}) + 15000$). Energy consumption is modeled and validated by combining empirical timing measurements from Wokwi (`micros()`) with reference power-consumption profiles across states (boot, Wi-Fi RX/OFF, deep sleep, and sensor readings). Furthermore, wireless multihop routing trade-offs in Wireless Sensor Networks (WSN) are evaluated analytically using an energy consumption path-loss model ($E_{tx}(k,d) = k E_c + k \epsilon d^2$).

### Technologies 
*	**Languages:** C++, Python
*	**Microcontroller:** ESP32
*	**Framework:** Arduino
*	**Simulator:** Wokwi
*	**Protocol:** ESP-NOW

## Challenge 2 - Packet Sniffing & Protocol Analysis

### Project Description
In-depth packet sniffing, traffic analysis, and protocol evaluation of constrained IoT messaging standards (CoAP, MQTT, and MQTT-SN) using real capture files (A.pcapng and B.pcapng).

### Technical Details
Analyzed message transactions, status codes, retransmissions, and publish broker interactions. This includes identifying successful non-confirmable CoAP DELETE requests, filtering CoAP observe notifications and resource behaviors, tracking MQTT-SN traffic, evaluating Last Will and Testament (LWT) messages with wildcards, and analyzing retained message erasure across public (HiveMQ) and local brokers. It also features a statistical analysis of topic depth distribution (histogram plotting of PUBLISH message layers) and a theoretical energy consumption evaluation comparing direct CoAP versus gateway-based MQTT communications under specific RTO and QoS 1 constraints.

### Technologies 
*	**Tools:** Wireshark
*	**Languages:** Python
*	**Libraries:** Pyshark, Scapy, Matplotlib
*	**Formats:** PCAPNG (Packet Capture)

## Challenge 3 - Node-RED & LoRaWAN Pipeline

### Project Description
Implementation of a data processing and automation pipeline using Node-RED alongside a theoretical analysis of LoRaWAN network performance.

### Technical Details
The Node-RED flow periodically generates random IDs and timestamps, publishing them via MQTT to a local Mosquitto broker while logging them to `id_log.csv`. A subscriber branch reads back the IDs, computes a modulo operation ($N = ID \pmod{5218}$) to map them to rows in a provided ZigBee dataset (`challenge3.csv`), and rate-limits processing to 10 msg/min. For matching ZBEE_ZCL layers, it structures and republishes device attributes. For RMS current, voltage, and active power attributes, it extracts, matches list positions, logs data to `filtered_elems.csv`, and visualizes them on real-time dashboards. For link status packets, it computes outgoing routing costs, logs them to `outgoing_cost.csv`, and periodically pushes the metrics to a public ThingSpeak cloud channel via HTTP API. The second part evaluates European LoRaWAN parameters (868 MHz, 125 kHz) using the TTN airtime calculator to find the optimal Spreading Factor (SF) ensuring $\ge 75\%$ packet success rate under Poisson traffic intensity.

### Technologies 
*	**Platform:** Node-RED
*	**Protocols:** MQTT, HTTP API
*	**Broker:** Mosquitto
*	**Cloud & Dashboard:** ThingSpeak API, Node-RED Dashboard
*	**Languages:** JavaScript (Node-RED functions), Python
*	**Data Formats:** CSV, JSON

## Homework - Theoretical and Practical Assignments

### Project Description
Comprehensive collection of theoretical exercises and practical assignments covering core networking, power consumption modeling, and communication protocols within IoT systems.

### Techincal Details
*	**Analytical Modeling:** Evaluation of power-consumption characteristics, energy budgets, and operational lifetimes for battery-powered IoT devices.

*	**Protocol & Network Optimization:** Assessment of trade-offs between direct node-to-node communications versus gateway-assisted architectures, analyzing metrics such as packet success rates, link budgets, and airtime calculations.

*	**Theoretical Problem Solving:** Detailed analytical derivations and mathematical solutions addressing specific wireless sensor network (WSN) challenges and routing efficiencies.

## Repository Structure
`challenge_X/src/`: Contains main source files for challenge X.

`challenge_X/docs/`: Includes original rules/specifications for challenge X.

`challenge_X/deliverables/`: Contains deliverables for challenge X.
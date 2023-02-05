# mqtt-energi
Protocol documentation and mqtt bridge for the myenergi device to device communications

## Introduction
This repository is meant to document reverse engineering attempts on the device-to-device communications used between myenergi devices for the purposes of intercepting them and posting the data to a local MQTT server. 

This has been tested on a V2.1 Eddi as that is the only device I have. It might be able to recieve packets from other myenergi devices, but cant do anything with them as it wont understand the format of the data. 

V1 devices (without an ethernet port or wifi) wont work at all as this relies on intercepting the device to device communications that happen over the network. 

## Disclaimer
This is a hobby project that is not affiliated with MyEnergi ltd in any way. Use at your own risk. All company and product names are copyright of their respective owners.

## Index
* [Communication Overview]
* [Data Packets Format]
* [MQTT Bridge]


[Data Packets Format]: docs/data_packets.md
[MQTT Bridge]: docs/mqtt_bridge.md
[Communication Overview]: docs/communication.md
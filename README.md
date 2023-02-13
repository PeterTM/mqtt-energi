# mqtt-energi
Protocol documentation myenergi device to device communications and mqtt bridge for local data access

## Introduction
This repository is meant to document reverse engineering attempts on the device-to-device communications used between myenergi devices for the purposes of intercepting them and posting the data to a local MQTT server. 

## Disclaimer
This is a hobby project that is not affiliated with MyEnergi ltd in any way. Use at your own risk. All company and product names are copyright of their respective owners.

## Current Capabilities
The MQTT Bridge can currently extract the following information from A V2.1 Eddi. It might be able to recieve packets from other myenergi devices, but cant do anything with them as it wont understand the format of the data. 

* Serial Number
* Supply Voltage
* Supply Frequency
* Grid Power
* Generation Power
* Diverting Power
* Total Diverted Energy per day. 
* Active heater channel
* Boost State

V1 devices (without an ethernet port or wifi) wont work at all as this relies on intercepting the device to device communications that happen over the network. 

## Index
* [Communication Overview]
* [Data Packets Format]
* [MQTT Bridge]


[Data Packets Format]: docs/data_packets.md
[MQTT Bridge]: docs/mqtt_bridge.md
[Communication Overview]: docs/communication.md
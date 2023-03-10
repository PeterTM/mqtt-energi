# MQTT Bridge
This is a quick and dirty script that captures the packets matching the ethertype and data header of the myenergi packets. This works by putting the PC's NIC into promiscuous mode and looking for packets that match the profile that we are looking for. Once it has found a packet, its payload is processed by the decoder. If the decoder understands the packet type, it will pull out the data and post it to a MQTT broker

## Compatibility
In its current form, this probably only works on linux based systems due to having to set the NIC mode to allow it to recieve all packets. Windows may work in the future if I get around to working out how. 

This has only been tested recieving the following data from a Eddi V2.1 unit. Other capabilities may follow if the protocol is better understood
* Current Supply Voltage / Frequency
* Current Grid Power / Generation Power / Divert Power
* Total Diverted Energy
* Active Heater Channel
* Boost & stopped status



## Setup
Your python installation needs paho.mqtt installed

in file config.ini, you need to set
* your broker IP and port
* the topic you want the data posted to
* a unique client ID
* the user/password for ypur mqtt broker (if needed)

 The data will be posted to 

> {topic}/{serialnumber}/{data}

You also need to set the name of the NIC that you are using to allow it to be bound and set to promisc mode. The script needs to be run with root permissions for the moment as it manipulates the NIC to set it to promiscuous mode. 

# Communication Overview
The devices appear to communicate with each other using a [layer 2](https://en.wikipedia.org/wiki/Data_link_layer) MAC multicast to the address '71:b3:d5:3a:6f:00'. 

The ethernet frame transmitted has an ethertype set of '0x88b5' which wireshark identifies as 'Local Experimental Ethertype 1'

The Payload of each frame appears to contain a common header containing a value that appears to signify the type of data within the packet, and then various lengths of data frame that contain information from the device in question (current understanding of these documented in [Data Packets Format])

As most networking stacks drop frames they are not interested in, to recieve and propcess the frames the NIC needs to be in [promiscuous mode](https://en.wikipedia.org/wiki/Promiscuous_mode) to allow user level processes to recieve and process the frames. There may be a more elegant way to signal the kernal that you want to recieve these frames but at this moment I am unsure how. 

## Packet Capture setup
I have used [Wireshark](https://www.wireshark.org/) to capture the data from the device. You can set it up to only look for the communication packets by using the filter below

> eth.type == 0x88b5 && eth.dst == 71:b3:d5:3a:6f:00

Once packets are captures, the payloads can be exported as bin files and analysed. 



[Data Packets Format]: ../docs/data_packets.md
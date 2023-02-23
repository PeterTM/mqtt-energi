# Packet Format
All packets are recieved as raw ethernet frames with a protocol set as type 0x88b5 which wireshark identifies as 'Local Experimental Ethertype 1'

Following the ethernet header, various types of data packets can be seen from coming from the device. 

## Header
All packets start with a 30 byte long header formatted as below

| Start Address | Size (Bytes) | Description        | Contents            |
|---------------|--------------|--------------------|---------------------|
|      0x00     |       4      | Packet Header?     | CB DA E9 F8         |
|      0x04     |      16      | Unknown (Padding?) | 0x00                |
|      0x14     |       1      | Unknown            | 0x01                |
|      0x15     |       3      | Unknown (Padding)  | 0x00                |
|      0x18     |       1      | Message Length     | Various (See Below) |
|      0x19     |       1      | Device Type ?      | Always 0x53         |
|      0x1A     |       2      | Message Type  1  ? |                     |
|      0x1B     |       2      | Message Type  2  ? |                     |

Various Types of packets have been observed so far. 
## Packet Types

| Packet Len  | Data Length (Bytes) | Contents                        | Transmit Rate (Seconds) |  Notes                       |
|-------------|---------------------|---------------------------------|-------------------------|------------------------------|
|     0x1F    |          55         | Eddi Data (Packet Type 1)       |            24           |                              |
|     0x20    |          56         | Eddi Data (Packet Type 2)       |            12           |                              |
|     0x2B    |          67         | Eddi Data (Packet Type 3)       |            12           | data not consistant          |
|     0x2C    |          68         | ??                              |            12           |                              |
|     0x2D    |          69         | ??                              |            12           |                              |
|     0x22    |          58         | CT Readings?                    |            2            |                              |
|     0x27    |          63         | Unknown                         |            4            |                              |
|     0x36    |          78         | Unknown                         |            2            |                              |
|     0x37    |          79         | Unknown                         |            tbc          |                              |
|     0x38    |          80         | Unknown                         |            tbc          |                              |
|     0x39    |          81         | Unknown                         |            tbc          |                              |
|     0x3a    |          82         | Unknown                         |            tbc          |                              |

The following Packets have been decoded (or partially decoded) so far

### 0x1F - Eddi Data (Packet Type 1)

Transmitted Approx Every 12 seconds

| Start Address | Size (Bytes) | Data Type | Description    | Post Processing |
|---------------|--------------|-----------|----------------|-----------------|
|      0x1E     |       4      |   int32   | Serial Number  | N/A             |
|      0x22     |       2      |   int16   | Grid Frequency | Divide by 100   |
|      0x2C     |       2      |   int16   | Diverted kWh   |   / 100         |
|      0x32     |       2      |   int16   | Voltage        | Divide by 10    |

###  0x20 - Eddi Data (Packet Type 2)

Transmitted Approx Every 24 seconds

| Start Address | Size (Bytes) | Data Type | Description          | Post Processing |
|---------------|--------------|-----------|----------------------|-----------------|
|      0x1E     |       4      |   int32   | Serial Number        | N/A             |
|      0x22     |       2      |   int16   | Grid Frequency       | Divide by 100   |
|      0x2C     |       2      |   int16   | Diverted kWh         |   / 100         |
|      0x24     |       2      |   bool    | Status Bit?          |                 |
|      0x26     |       2      |   int16   | Max Heater Power (*1)|                 |
|      0x34     |       2      |   int16   | Divert Power         |   / 100         |
|      0x36     |       2      |   int16   | Divert Current?      |   / 100         |
|      0x2E.0   |       1      | bool      | Boosting             |  N/A            |
|      0x2F.7   |       1      | bool      | Heater 1 Active      |  N/A            |
|      0x2F.6   |       1      | bool      | Heater 2 Active      |  N/A            |
|      0x2F.5   |       1      | bool      | unknown              |  N/A            |
|      0x2F.4   |       1      | bool      | unknown              |  N/A            |
|      0x2F.3   |       1      | bool      | unknown              |  N/A            |
|      0x2F.2   |       1      | bool      | unknown              |  N/A            |
|      0x2F.1   |       1      | bool      | unknown              |  N/A            |
|      0x2F.0   |       1      | bool      | unknown              |  N/A            |
|      0x25.7   |       1      | bool      | Stopped Mode         |  N/A            |


1. Appears to be the maximum heater power that is connected to the active channel. For example, if you had a 3kW heater then this would read 3000. Sits at maximum rated power (3600) when nothing is connected or channel is off. 

### 0x2B - Eddi Data (Packet Type 3)

Transmitted approx ever 12 seconds

| Start Address | Size (Bytes) | Data Type | Description                                             | Post Processing |
|---------------|--------------|-----------|---------------------------------------------------------|-----------------|
|      0x1E     |       4      |   int32   | Serial Number                                           | N/A             |
|      0x22     |       2      |   int16   | Frequency                                               | Divide by 100   |
|      0x2C     |       2      |   int16   | Diverted kwH                                            | Divide by 100   | 
|      0x3C     |       2      |   int16   | Generation Power                                        |                 |
|      0x34     |       2      |   int16   | Grid Power                                              |                 |


### 0x22 - CT Readings?

Transmitted Approx ever 2 seconds

| Start Address | Size (Bytes) | Data Type | Description      | Post Processing |
|---------------|--------------|-----------|------------------|-----------------|
|      0x1E     | 2            |   int16   | Grid Power       | N/A             |
|      0x22     | 2            |   int16   | Generation Power | N/A             |
|      0x32     | 2            |   int16   | Diverting Power  | N/A             |
|      0x2E     | 4            |   int32   | Serial Number    | N/A             |


### 0x27 - Unknown

Transmitted approx every 4 seconds

| Start Address | Size (Bytes) | Data Type | Description                                             | Post Processing |
|---------------|--------------|-----------|---------------------------------------------------------|-----------------|
|      0x1E     |       4      |   int32   | Serial Number                                           | N/A             |
|      0x22     |       2      |   int16   | Grid Frequency                                          | Divide by 100   |
|      0x2C     |       2      |   int16   | Diverted kWh                                            |   / 100         |
|      0x36     |       2      |   int16   | Firmware Version (But appears to occasionally go blank) |                 | 
|      0x38     |       2      |   int16   | Firmware Version2(But appears to occasionally go blank) |                 |
|      0x3A     |       2      |   int16   | Unknown                                                 |                 | 
|      0x3D     |       2      |   int16   | Unknown. Seems to track diverter power but not exactly  |                 |


### 0x36 - Unknown

Transmitted approx every 2 seconds

| Start Address | Size (Bytes) | Data Type | Description                                             | Post Processing |
|---------------|--------------|-----------|---------------------------------------------------------|-----------------|
|      0x4A     |       4      |   int32   | Serial Number                                           | N/A             |
|      0x3A     |       2      |   int16   | Frequency (Seems to update faster than 0x1F)            |                 | 
|      0x38     |       2      |   int16   | Voltage (Seems to update faster than 0x1F)              |                 |

### 0x37 - Unknown


| Start Address | Size (Bytes) | Data Type | Description                                             | Post Processing |
|---------------|--------------|-----------|---------------------------------------------------------|-----------------|
|      0x1E     |       4      |   int32   | Serial Number                                           | N/A             |


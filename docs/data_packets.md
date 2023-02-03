All packets are recieved as raw ethernet frames with a protocol set as type 0x88b5 which wireshark identifies as 'Local Experimental Ethertype 1'

Following the ethernet header, various types of data packets can be seen from coming from the device. 

All packets start with a 19 byte long header formatted as below

| Start Address | Size (Bytes) | Description        | Contents            |
|---------------|--------------|--------------------|---------------------|
|      0x00     |       4      | Packet Header?     | CB DA E9 F8         |
|      0x04     |      16      | Unknown (Padding?) | 0x00                |
|      0x14     |       1      | Unknown            | 0x01                |
|      0x15     |       3      | Unknown (Padding)  | 0x00                |
|      0x18     |       1      | Packet Type ?      | Various (See Below) |
|      0x19     |       1      | Device Type ?      | Always 0x53         |

Various Types of packets have been observed so far. 

| Packet Type | Data Length (Bytes) | Contents                        |
|-------------|---------------------|---------------------------------|
|     0x1F    |          55         | Frequency & Voltage Information |
|     0x20    |          56         | Energy Info                     |
|     0x22    |          58         | Generation & Grid Power         |
|     0x27    |          63         | Unknown                         |
|     0x2B    |          67         | Unknown                         |
|     0x36    |          78         | Unknown                         |
|     0x37    |          79         | Unknown                         |
|     0x38    |          80         | Unknown                         |
|     0x39    |          81         | Unknown                         |

The following Packets have been decoded (or partially decoded) so far

## 0x1F - Frequecny & Voltage

| Start Address | Size (Bytes) | Data Type | Description    | Post Processing |
|---------------|--------------|-----------|----------------|-----------------|
|      0x1E     | 4            |   int32   | Serial Number  | N/A             |
|      0x22     | 2            |   int16   | Grid Frequency | Divide by 100   |
|      0x32     | 2            |   int16   | Voltage        | Divide by 10    |

## 0x22 - Generation and Grid


| Start Address | Size (Bytes) | Data Type | Description      | Post Processing |
|---------------|--------------|-----------|------------------|-----------------|
|      0x1E     | 2            |   int16   | Grid Power       | N/A             |
|      0x22     | 2            |   int16   | Generation Power | N/A             |
|      0x32     | 2            |   int16   | Diverting Power  | N/A             |
|      0x2E     | 4            |   int32   | Serial Number    | N/A             |

## 0x20 - Unknown

| Start Address | Size (Bytes) | Data Type | Description   | Post Processing |
|---------------|--------------|-----------|---------------|-----------------|
|      0x1E     |       4      |   int32   | Serial Number | N/A             |
|      0x2C     |       2      |   int16   | Diverted kWh  |   / 1000        |


## 0x27 - Unknown

| Start Address | Size (Bytes) | Data Type | Description   | Post Processing |
|---------------|--------------|-----------|---------------|-----------------|
|      0x1E     |       4      |   int32   | Serial Number | N/A             |
|      0x22     |       2      |   int16   | Frequency??   |                 |
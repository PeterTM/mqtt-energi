import struct

def status_decode(inbyte):
    return [1 if inbyte & (1 << (7-n)) else 0 for n in range(8)]


def decode_packet(eth_pkt,debug):
    packet_len = len(eth_pkt)
    packet_type = eth_pkt[0x18]
    data = {}

    if packet_type == 0x1F: # Frequency Message
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        freq = int.from_bytes(eth_pkt[0x22:0x24], "little")
        div_wh = int.from_bytes(eth_pkt[0x2c:0x2e], "little")
        voltage = int.from_bytes(eth_pkt[0x32:0x34], "little")
        data = {
            'serial':serialno,
            'frequency':freq/100,
            'voltage':voltage/10,
            'diverted_kWh':div_wh/100
        }

    elif packet_type == 0x20: # Diverter Data?
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        div_wh = int.from_bytes(eth_pkt[0x2c:0x2e], "little")
        divert_pwr = int.from_bytes(eth_pkt[0x34:0x36], "little")
        divert_cur = int.from_bytes(eth_pkt[0x36:0x38], "little") # not sure about this
        max_power = int.from_bytes(eth_pkt[0x26:0x28], "little") # not sure about this
        status = status_decode(int(eth_pkt[0x2F]))
        status2 = status_decode(int(eth_pkt[0x25]))
        status3 = status_decode(int(eth_pkt[0x2E]))
        heater1 = status[7]
        heater2 = status[6]
        boost = status3[3]
        stopped = status2[0]

        data = {
            'serial':serialno,
            'diverted_kWh':div_wh/100,
            'divert_pwr':divert_pwr,
            #'divert_cur':divert_cur,
            'heater1':heater1,
            'heater2':heater2,
            'stopped':stopped,
            'boost':boost,
            #'max_power':max_power
        }
    elif packet_type == 0x2B: #Data ?
            serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
            freq = int.from_bytes(eth_pkt[0x22:0x24], "little") 
            div_wh = int.from_bytes(eth_pkt[0x2c:0x2e], "little")
            gen_pow = int.from_bytes(eth_pkt[0x3c:0x3e], "little",signed=True) # occasionally goes zero
            grid_pow = int.from_bytes(eth_pkt[0x34:0x36], "little", signed=True) #occasionally goes to weird value
            div_pow = int.from_bytes(eth_pkt[0x41:0x43], "little", signed=True)
            v1 = int.from_bytes(eth_pkt[0x41:0x43], "little",signed=True) # proportional to generation
            if debug:
                data = {
                    'serial':serialno,
                    'frequency':freq/100,
                    'diverted_kWh':div_wh/100,
                    #'gen_pwr':gen_pow,
                    #'grid_pwr':grid_pow,
                    'divert_pwr':div_pow,
                    }

    elif packet_type == 0x22: # CT Readings
        gen_pow = int.from_bytes(eth_pkt[0x22:0x24], "little",signed=True) # Generation Power
        grid_pow = int.from_bytes(eth_pkt[0x1e:0x20], "little", signed=True) # Grid Power
        div_pow = int.from_bytes(eth_pkt[0x32:0x34], "little", signed=True) # Diverter Power
        serialno = int.from_bytes(eth_pkt[0x2e:0x32], "little") # Serial No
        data = {
            'serial':serialno,
            'gen_pwr':gen_pow,
            'grid_pwr':grid_pow,
            'divert_pwr':div_pow,
        }



    

    elif packet_type == 0x27: #Data ?
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        freq = int.from_bytes(eth_pkt[0x22:0x24], "little") 
        div_wh = int.from_bytes(eth_pkt[0x2c:0x2e], "little")
        fw1 = int.from_bytes(eth_pkt[0x38:0x3A], "little",signed=True)
        fw2 = int.from_bytes(eth_pkt[0x36:0x38], "little",signed=True)
        v1 = int.from_bytes(eth_pkt[0x3d:0x3e], "little",signed=True) # seems to track diverter power but not exactly. possibly output voltage?
        v2 = int.from_bytes(eth_pkt[0x3c:0x3d], "little",signed=True)
        v3 = int.from_bytes(eth_pkt[0x3A:0x3C], "little",signed=True) 
        v4 = int.from_bytes(eth_pkt[0x34:0x36], "little",signed=True) 
        v5 = int.from_bytes(eth_pkt[0x32:0x34], "little",signed=True) 
        v6 = int.from_bytes(eth_pkt[0x30:0x32], "little",signed=True) 
        v7 = int.from_bytes(eth_pkt[0x2E:0x30], "little",signed=True)
        if debug:
            data = {
                'serial':serialno,
                'frequency':freq/100,
                'diverted_kWh':div_wh/100,
                '0x27/fw1':fw1,
                '0x27/fw2':fw2,
                '0x27/v1':v1,
                '0x27/v2':v2,
                '0x27/v3':v3,
                '0x27/v4':v4,
                '0x27/V5':v5,
                '0x27/v6':v6,
                '0x27/v7':v7
            }
        

    elif packet_type == 0x37: # Divert Power
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        v1 = int.from_bytes(eth_pkt[0x4D:0x4F], "little",signed=True) # diverter power?
        v2 = int.from_bytes(eth_pkt[0x3c:0x3d], "little",signed=True)
        v3 = int.from_bytes(eth_pkt[0x3A:0x3C], "little",signed=True) 
        v4 = int.from_bytes(eth_pkt[0x34:0x36], "little",signed=True) 
        v5 = int.from_bytes(eth_pkt[0x32:0x34], "little",signed=True) 
        v6 = int.from_bytes(eth_pkt[0x30:0x32], "little",signed=True) 
        v7 = int.from_bytes(eth_pkt[0x2E:0x30], "little",signed=True)
        if debug:
            data = {
                'serial':serialno,
                '0x27/v1':v1,
                '0x27/v2':v2,
                '0x27/v3':v3,
                '0x27/v4':v4,
                '0x27/V5':v5,
                '0x27/v6':v6,
                '0x27/v7':v7
            }

    elif packet_type == 0x36: # ?
        serialno = int.from_bytes(eth_pkt[0x4A:0x4E], "little")

        v1 = int.from_bytes(eth_pkt[0x1C:0x1E], "little",signed=True)
        v2 = int.from_bytes(eth_pkt[0x1E:0x20], "little",signed=True) 
        v3 = int.from_bytes(eth_pkt[0x20:0x22], "little",signed=True) 
        v4 = int.from_bytes(eth_pkt[0x22:0x24], "little",signed=True) 
        v5 = int.from_bytes(eth_pkt[0x24:0x26], "little",signed=True) 
        v6 = int.from_bytes(eth_pkt[0x30:0x32], "little",signed=True)
        v7 = int.from_bytes(eth_pkt[0x34:0x36], "little",signed=True)
        v8 = int.from_bytes(eth_pkt[0x36:0x38], "little",signed=True)
        v9 = int.from_bytes(eth_pkt[0x38:0x3A], "little",signed=True) # Voltage?
        v10 = int.from_bytes(eth_pkt[0x3A:0x3C], "little",signed=True) # Frequency
        v11 = int.from_bytes(eth_pkt[0x3C:0x3E], "little",signed=True) # Heatsink Temp
        v12 = int.from_bytes(eth_pkt[0x3E:0x40], "little",signed=True)
        v13 = int.from_bytes(eth_pkt[0x40:0x42], "little",signed=True)
        v14 = int.from_bytes(eth_pkt[0x42:0x44], "little",signed=True)
        v15 = int.from_bytes(eth_pkt[0x44:0x46], "little",signed=True)
        v16 = int.from_bytes(eth_pkt[0x46:0x48], "little",signed=True)
        v17 = int.from_bytes(eth_pkt[0x48:0x4A], "little",signed=True)
        if debug:
            data = {
                'serial':serialno,
                '0x36/v1':v1,
                '0x36/v2':v2,
                '0x36/v3':v3,
                '0x36/v4':v4,
                '0x36/v5':v5,
                '0x36/v6':v6,
                '0x36/v7':v7,
                '0x36/v8':v8,
                '0x36/v9':v9,
                '0x36/v10':v10,
                '0x36/v11':v11,
                '0x36/v12':v12,
                '0x36/v13':v13,
                '0x36/v14':v14,
                '0x36/v15':v15,
                '0x36/v16':v16,
                '0x36/v17':v17

            }
    elif packet_type == 0x38: # ?
        serialno = int.from_bytes(eth_pkt[0x1E:0x22], "little")
        v1 = int.from_bytes(eth_pkt[0x20:0x22], "little",signed=True)
        v2 = int.from_bytes(eth_pkt[0x22:0x24], "little",signed=True)
        v3 = int.from_bytes(eth_pkt[0x24:0x26], "little",signed=True) # Frequency
        v4 = int.from_bytes(eth_pkt[0x26:0x28], "little",signed=True) # Voltage?
        v5 = int.from_bytes(eth_pkt[0x28:0x2A], "little",signed=True)
        v6 = int.from_bytes(eth_pkt[0x2A:0x2C], "little",signed=True)
        v7 = int.from_bytes(eth_pkt[0x2C:0x2E], "little",signed=True)
        v8 = int.from_bytes(eth_pkt[0x2E:0x30], "little",signed=True)
        v9 = int.from_bytes(eth_pkt[0x30:0x32], "little",signed=True)
        v10 = int.from_bytes(eth_pkt[0x32:0x34], "little",signed=True)
        v11 = int.from_bytes(eth_pkt[0x34:0x36], "little",signed=True)
        v12 = int.from_bytes(eth_pkt[0x36:0x38], "little",signed=True)
        v13 = int.from_bytes(eth_pkt[0x38:0x3A], "little",signed=True)
        v14 = int.from_bytes(eth_pkt[0x3A:0x3C], "little",signed=True)
        v15 = int.from_bytes(eth_pkt[0x3C:0x3E], "little",signed=True)
        v16 = int.from_bytes(eth_pkt[0x3E:0x40], "little",signed=True)
        if debug:
            data = {
                'serial':serialno,
                '0x38/v1':v1,
                '0x38/v2':v2,
                '0x38/v3':v3,
                '0x38/v4':v4,
                '0x38/v5':v5,
                '0x38/v6':v6,
                '0x38/v7':v7,
                '0x38/v8':v8,
                '0x38/v9':v9,
                '0x38/v10':v10,
                '0x38/v11':v11,
                '0x38/v12':v12,
                '0x38/v13':v13,
                '0x38/v14':v14,
                '0x38/v15':v15,
                '0x38/v16':v16

            }

    elif packet_type == 0x3A: # ?
            serialno = int.from_bytes(eth_pkt[0x1E:0x22], "little")
            v2 = int.from_bytes(eth_pkt[0x22:0x24], "little",signed=True)
            v3 = int.from_bytes(eth_pkt[0x24:0x26], "little",signed=True) 
            v4 = int.from_bytes(eth_pkt[0x26:0x28], "little",signed=True) 
            v5 = int.from_bytes(eth_pkt[0x28:0x2A], "little",signed=True)
            v6 = int.from_bytes(eth_pkt[0x2A:0x2C], "little",signed=True)
            v7 = int.from_bytes(eth_pkt[0x2C:0x2E], "little",signed=True)
            v8 = int.from_bytes(eth_pkt[0x2E:0x30], "little",signed=True)
            v9 = int.from_bytes(eth_pkt[0x30:0x32], "little",signed=True)
            v10 = int.from_bytes(eth_pkt[0x32:0x34], "little",signed=True)
            v11 = int.from_bytes(eth_pkt[0x34:0x36], "little",signed=True)
            v12 = int.from_bytes(eth_pkt[0x36:0x38], "little",signed=True)
            v13 = int.from_bytes(eth_pkt[0x38:0x3A], "little",signed=True)
            v14 = int.from_bytes(eth_pkt[0x44:0x46], "little",signed=True)
            v15 = int.from_bytes(eth_pkt[0x42:0x44], "little",signed=True)
            if debug:
                data = {
                    'serial':serialno,
                    '0x3A/v2':v2,
                    '0x3A/v3':v3,
                    '0x3A/v4':v4,
                    '0x3A/v5':v5,
                    '0x3A/v6':v6,
                    '0x3A/v7':v7,
                    '0x3A/v8':v8,
                    '0x3A/v9':v9,
                    '0x3A/v10':v10,
                    '0x3A/v11':v11,
                    '0x3A/v12':v12,
                    '0x3A/v13':v13,
                    '0x3A/v14':v14,
                    '0x3A/v15':v15,

                }


    else:
        dummy = True    
        #print(f'type:{hex(packet_type)}, Packet Length: {packet_len} [UNIMPLEMENTED]')
    return data

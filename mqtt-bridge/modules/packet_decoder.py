

def decode_packet(eth_pkt,debug):
    packet_len = len(eth_pkt)
    packet_type = eth_pkt[0x18]
    data = {}

    if packet_type == 0x1F: # Frequency Message
        freq = int.from_bytes(eth_pkt[0x22:0x24], "little")/100
        voltage = int.from_bytes(eth_pkt[0x32:0x34], "little")/10
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        data = {
            'serial':serialno,
            'frequency':freq,
            'voltage':voltage
        }

    elif packet_type == 0x22: # Generation Message
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

    elif packet_type == 0x20: # Diverter Data?
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        div_wh = int.from_bytes(eth_pkt[0x2c:0x2e], "little")
        data = {
            'serial':serialno,
            'diverted_kWh':div_wh/100
        }

    elif packet_type == 0x2B: #Data ?
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        v1 = int.from_bytes(eth_pkt[0x20:0x22], "little") 
        v2 = int.from_bytes(eth_pkt[0x22:0x24], "little") # Frequency
        v3 = int.from_bytes(eth_pkt[0x24:0x26], "little") 
        v4 = int.from_bytes(eth_pkt[0x26:0x28], "little") 
        v5 = int.from_bytes(eth_pkt[0x28:0x2A], "little") 
        v6 = int.from_bytes(eth_pkt[0x2A:0x2C], "little") 
        v7 = int.from_bytes(eth_pkt[0x2C:0x2E], "little")
        v8 = int.from_bytes(eth_pkt[0x2E:0x30], "little")
        v9 = int.from_bytes(eth_pkt[0x30:0x32], "little")
        v10 = int.from_bytes(eth_pkt[0x32:0x34], "little")
        v11 = int.from_bytes(eth_pkt[0x34:0x36], "little")
        v12 = int.from_bytes(eth_pkt[0x36:0x38], "little")
        v13 = int.from_bytes(eth_pkt[0x38:0x3A], "little")
        v14 = int.from_bytes(eth_pkt[0x3A:0x3C], "little")
        v15 = int.from_bytes(eth_pkt[0x3C:0x3E], "little") # Generation Power?
        v16 = int.from_bytes(eth_pkt[0x3E:0x40], "little")
        v17 = int.from_bytes(eth_pkt[0x40:0x43], "little")
        if debug:
            data = {
                'serial':serialno,
                '0x2B/v1':v1,
                '0x2B/v2':v2,
                '0x2B/v3':v3,
                '0x2B/v4':v4,
                '0x2B/v5':v5,
                '0x2B/v6':v6,
                '0x2B/v7':v7, 
                '0x2B/v8':v8,
                '0x2B/v9':v9,
                '0x2B/v10':v10,
                '0x2B/v11':v11,
                '0x2B/v12':v12,
                '0x2B/v13':v13,
                '0x2B/v14':v14,
                '0x2B/v15':v15,
                '0x2B/v16':v16,
                '0x2B/v17':v17
            }

    elif packet_type == 0x27: #Data ?
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        fw1 = int.from_bytes(eth_pkt[0x38:0x3A], "little")
        fw2 = int.from_bytes(eth_pkt[0x36:0x38], "little")
        v1 = int.from_bytes(eth_pkt[0x3d:0x3e], "little") # seems to track diverter power but not exactly. possibly output voltage?
        v2 = int.from_bytes(eth_pkt[0x3c:0x3d], "little")
        v3 = int.from_bytes(eth_pkt[0x3A:0x3C], "little") 
        v4 = int.from_bytes(eth_pkt[0x34:0x36], "little") 
        v5 = int.from_bytes(eth_pkt[0x32:0x34], "little") 
        v6 = int.from_bytes(eth_pkt[0x30:0x32], "little") 
        v7 = int.from_bytes(eth_pkt[0x2E:0x30], "little")
        if debug:
            data = {
                'serial':serialno,
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
        v1 = int.from_bytes(eth_pkt[0x4D:0x4F], "little") # diverter power?

    elif packet_type == 0x36: # ?
        serialno = int.from_bytes(eth_pkt[0x4A:0x4E], "little")
        v1 = int.from_bytes(eth_pkt[0x3C:0x3E], "little")
        v2 = int.from_bytes(eth_pkt[0x44:0x46], "little")
        v3 = int.from_bytes(eth_pkt[0x3A:0x3C], "little") # Frequency
        v4 = int.from_bytes(eth_pkt[0x38:0x3A], "little") # Voltage?
        v5 = int.from_bytes(eth_pkt[0x36:0x38], "little")
        v6 = int.from_bytes(eth_pkt[0x30:0x32], "little")
        v7 = int.from_bytes(eth_pkt[0x26:0x28], "little")
        v8 = int.from_bytes(eth_pkt[0x24:0x26], "little")
        v9 = int.from_bytes(eth_pkt[0x22:0x24], "little")
        if debug:
            data = {
                'serial':serialno,
                '0x36/v1':v1,
                '0x36/v2':v2,
                '0x36/v3':v3,
                '0x36/v4':v4/10,
                '0x36/v5':v5,
                '0x36/v6':v6,
                '0x36/v7':v7,
                '0x36/v8':v8,
                '0x36/v9':v9,

            }


    else:
        dummy = True    
        #print(f'type:{hex(packet_type)}, Packet Length: {packet_len} [UNIMPLEMENTED]')
    return data



def decode_packet(eth_pkt):
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
        gen_pow = int.from_bytes(eth_pkt[0x22:0x24], "little",signed=True)
        grid_pow = int.from_bytes(eth_pkt[0x1e:0x20], "little", signed=True)
        div_pow = int.from_bytes(eth_pkt[0x32:0x34], "little", signed=True)
        serialno = int.from_bytes(eth_pkt[0x2e:0x32], "little")
        data = {
            'serial':serialno,
            'gen_pwr':gen_pow,
            'grid_pwr':grid_pow,
            'divert_pwr':div_pow
        }

    elif packet_type == 0x20: # Diverter Data?
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        div_wh = int.from_bytes(eth_pkt[0x2c:0x2e], "little")
        data = {
            'serial':serialno,
            'diverted_kWh':div_wh/100
        }

    elif packet_type == 0x27: #Data ?
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        fw1 = int.from_bytes(eth_pkt[0x38:0x3A], "little")
        fw2 = int.from_bytes(eth_pkt[0x36:0x38], "little")
        # data = {
        #     'serial':serialno,
        #     'firmware1':fw1,
        #     'firmware2':fw2
        # }

    elif packet_type == 0x2b: # ?
        serialno = int.from_bytes(eth_pkt[0x1e:0x22], "little")
        unknown = int.from_bytes(eth_pkt[0x22:0x24], "little")
        unknown2 = int.from_bytes(eth_pkt[0x32:0x34], "little")
        #print(f'type:{hex(packet_type)}, Packet Length: {packet_len},???: {unknown},???2: {unknown2} , Serial: {serialno}')

    elif packet_type == 0x36: # ?
        serialno = int.from_bytes(eth_pkt[0x4A:0x4E], "little")
        u1 = int.from_bytes(eth_pkt[0x30:0x33], "little")
        u2 = int.from_bytes(eth_pkt[0x36:0x38], "little")
        u3 = int.from_bytes(eth_pkt[0x38:0x3A], "little")
        u4 = int.from_bytes(eth_pkt[0x3A:0x3C], "little")
        u5 = int.from_bytes(eth_pkt[0x20:0x22], "little")
        u6 = int.from_bytes(eth_pkt[0x22:0x24], "little")
        u7 = int.from_bytes(eth_pkt[0x28:0x30], "little")

        mysterydata = [u1,u2,u3,u4,u5,u6,u7]
        #print(f'type:{hex(packet_type)}, Packet Length: {packet_len},???: {mysterydata} , Serial: {serialno}')

    else:
        dummy = True    
        #print(f'type:{hex(packet_type)}, Packet Length: {packet_len} [UNIMPLEMENTED]')
    return data

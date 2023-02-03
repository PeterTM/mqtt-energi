import socket
import selectors
import struct
import promisc
import atexit
from paho.mqtt import client as mqtt_client


NIC = "eno1"
MAC = b'\x94\xe6\x86\xa2\x8b@'

DATA_HEADER = (0xcb,0xda,0xe9,0xf8) # Myenergi packet header
ETH_P_ALL = 0x0003          # Every packet 
ETH_FRAME_LEN = 1514        # Ethernet frame len
ETH_HLEN = 14               # Ethernet header len
PKT_TYPE = 0x88b5           # Experimental Ethertype 1

MQTT_BROKER = '10.87.90.6'
MQTT_PORT = 1883
MQTT_TOPIC = 'myenergi'

client_id = f'myenergy-mqtt-1'

def connect_mqtt(broker,port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    mqtt = mqtt_client.Client(client_id)
    mqtt.on_connect = on_connect
    mqtt.connect(broker, port)
    return mqtt




def exit_handler():
    promisc.set(NIC,False) # Kick NIC back out of promisc mode on exit


atexit.register(exit_handler)

def generic_decoder(pkt,len):
    pkt_len = len - 26
    pkt_data = pkt[27:]
    if (pkt_len % 2) != 0:
        pkt_len = pkt_len -1
    struct_fmt = f'{int(pkt_len/2)}h'
    print(struct_fmt)
    data = struct.unpack(struct_fmt,pkt_data)
    print(data)


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
            'diverted_kWh':div_wh/1000
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






def main():
    mqtt = connect_mqtt(MQTT_BROKER, MQTT_PORT)
    mqtt.loop_start()
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL)) as server_socket: #Recoeve Raw Frames
        server_socket.bind((NIC, 0))
        promisc.set(NIC,True)
        with selectors.DefaultSelector() as selector:
            selector.register(server_socket.fileno(), selectors.EVENT_READ)
            while True: # Loop FOrever
                ready = selector.select()
                if ready:
                    frame = server_socket.recv(ETH_FRAME_LEN) # get ethernet frame
                    header = frame[:ETH_HLEN] # split header from frame
                    dest, source, protocol = struct.unpack('!6s6sH', header) #unpack header
                    payload = frame[ETH_HLEN:] # unpack payload
                    if protocol == PKT_TYPE:
                        start = struct.unpack('4B',payload[:4])
                        if start == DATA_HEADER:
                            data = decode_packet(payload)
                            if data:
                                print(data)
                            for key in data:
                                mqtt.publish(MQTT_TOPIC+"/"+str(data['serial'])+"/"+key, data[key])


        


if __name__ == '__main__':
    main()
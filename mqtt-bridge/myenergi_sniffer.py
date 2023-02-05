import socket
import selectors
import struct
from modules import constants
from modules import promisc
from modules.packet_decoder import decode_packet
from modules import mqtt_handler
from modules import configuration

import atexit

settings = configuration.read()

def exit_handler():
    promisc.set(settings['NETWORK']['NIC'],False) # Kick NIC back out of promisc mode on exit


atexit.register(exit_handler)

def main():
    mqtt = mqtt_handler.connect(settings['MQTT']['BROKER'], int(settings['MQTT']['PORT']))
    mqtt.loop_start()
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(constants.PKT_TYPE)) as server_socket: #Recieve Raw Frames
        server_socket.bind((settings['NETWORK']['NIC'], 0))
        promisc.set(settings['NETWORK']['NIC'],True) # set NIC to promiscuous mode
        with selectors.DefaultSelector() as selector:
            selector.register(server_socket.fileno(), selectors.EVENT_READ)
            while True: # Loop Forever
                ready = selector.select()
                if ready:
                    frame = server_socket.recv(constants.ETH_FRAME_LEN) # get ethernet frame
                    header = frame[:constants.ETH_HLEN] # split header from frame
                    dest, source, protocol = struct.unpack('!6s6sH', header) #unpack header
                    payload = frame[constants.ETH_HLEN:] # unpack payload
                    if protocol == constants.PKT_TYPE:
                        start = struct.unpack('4B',payload[:4])
                        if start == constants.DATA_HEADER:
                            data = decode_packet(payload)
                            if data:
                                print(data)
                            for key in data:
                                mqtt.publish(settings['MQTT']['TOPIC']+"/"+str(data['serial'])+"/"+key, data[key])


        


if __name__ == '__main__':
    main()
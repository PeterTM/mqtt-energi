import ctypes
import fcntl
from socket import AF_NETLINK, SOCK_DGRAM, socket

IFF_PROMISC = 0x100
SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914


class ifreq(ctypes.Structure):
    _fields_ = [("ifr_ifrn", ctypes.c_char * 16),
                ("ifr_flags", ctypes.c_short)]




def set(nic,state):
        ifr = ifreq()
        ifr.ifr_ifrn = str.encode(nic)
        s = socket(AF_NETLINK, SOCK_DGRAM)
        fcntl.ioctl(s.fileno(), SIOCGIFFLAGS, ifr) # G for Get
        if state:
            ifr.ifr_flags |= IFF_PROMISC
        else:
            ifr.ifr_flags &= ~IFF_PROMISC
        fcntl.ioctl(s.fileno(), SIOCSIFFLAGS, ifr) # S for Set
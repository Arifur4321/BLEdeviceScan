from scapy.all import *

def handle_packet(packet):
    if packet.haslayer(Dot11InformationElement) and packet[Dot11InformationElement].ID == 221:
        # Check if the packet is a RID packet (ID = 221)
        rid = packet[Dot11InformationElement].info
        print("RID packet:", rid)

# Start capturing packets on the specified interface
interface = "wlan0"
sniff(iface=interface, prn=handle_packet)
"""
Wifi Sniffer
"""

import os
from scapy.all import *

if len(sys.argv) ==  2:
	iface = str(sys.argv[1])
else:
	iface = "wlan0"

os.system("ifconfig " + iface + " down") 
os.system("iwconfig " + iface + " mode monitor")
os.system("ifconfig " + iface + " up")

def packet_info(pkt):
    bssid = pkt[Dot11].addr3
    p = pkt[Dot11Elt]
    cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                      "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
    ssid, channel = None, None
    crypto = set()
    while isinstance(p, Dot11Elt):
        if p.ID == 0:
            ssid = p.info
        elif p.ID == 3:
            channel = ord(p.info)
        elif p.ID == 48:
            crypto.add("WPA2")
        elif p.ID == 221 and p.info.startswith('\x00P\xf2\x01\x01\x00'):
            crypto.add("WPA")
        p = p.payload
    if not crypto:
        if 'privacy' in cap:
            crypto.add("WEP")
        else:
            crypto.add("OPN")
    print "    %r [%s], %s" % (ssid, bssid,' / '.join(crypto) )



def handle_packet(packet):
	if not packet.haslayer(Dot11Beacon) and not packet.haslayer(Dot11ProbeReq) and not packet.haslayer(Dot11ProbeResp):
		#regular packet
		print "    " + packet.summary()
		if packet.haslayer(Raw):
			print "\n"
			print hexdump(packet.load)
			print "\n"	
	elif packet.haslayer(Dot11ProbeReq) or packet.haslayer(Dot11ProbeResp) or packet.haslayer(Dot11AssoReq):
		#http://stackoverflow.com/questions/21613091/how-to-use-scapy-to-determine-wireless-encryption-type
		packet_info(packet)
		

print "[+] Sniffing on interface " + iface + ": "

while True:
	for channel in range(1, 14):
		os.system("iwconfig " + iface + " channel " + str(channel))
		print "[+] Sniffing on channel " + str(channel)

		sniff(iface=iface, prn=handle_packet, count=10, timeout=3, store=0)
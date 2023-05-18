#!/usr/bin/env python3

import codecs
from scapy.all import *


def handler(p):
    if not (p.haslayer(Dot11ProbeResp) or p.haslayer(Dot11ProbeReq) or p.haslayer(Dot11Beacon)):
        return

    rssi = p[RadioTap].dBm_AntSignal
    dst_mac = p[Dot11].addr1
    src_mac = p[Dot11].addr2
    ap_mac = p[Dot11].addr2
    info = f"rssi={rssi:2}dBm, dst={dst_mac}, src={src_mac}, ap={ap_mac}"

    if p.haslayer(Dot11ProbeResp):
        ssid = codecs.decode(p[Dot11Elt].info, 'utf-8')
        channel = ord(p[Dot11Elt:3].info)
        print(f"[ProbResp] {info}, chan={channel}, ssid=\"{ssid}\"")
    elif p.haslayer(Dot11ProbeReq):
        print(f"[ProbReq ] {info}")
    elif p.haslayer(Dot11Beacon):
        stats = p[Dot11Beacon].network_stats()
        ssid = str(stats['ssid'])
        channel = ord(p[Dot11Elt:3].info)
        interval = p[Dot11Beacon].beacon_interval
        print(f"[Beacon  ] {info}, chan={channel}, interval={interval}, ssid=\"{ssid}\"")


if __name__ == "__main__":
    sniff(iface="wlan1", prn=handler, store=0)
#!/usr/bin/python
#
# A very simple python-pcapy example for monitor mode WiFi sniffing.
#
# Usage example:
#   $ python pcapySniffer.py mon0

import pcapy
import sys
import os
import datetime


def main():
    if len(sys.argv) != 2:
        print ("Available devices:")
        print 
        devices = pcapy.findalldevs()

        for device in devices:
            print (device)

        print
        print ("Usage: ./%s deviceName"), sys.argv[0]
        exit()

    dev = sys.argv[1]

    print ("Trying to set monitor mode for device ") + dev + "..."
    os.system("ifconfig " + dev + " down")
    os.system("iwconfig " + dev + " mode monitor")
    os.system("ifconfig " + dev + " up")
    print ("Done. If you don't see any data, the monitor mode setup may have failed.")

    cap = pcapy.open_live(dev, 65536, True, 0)

    print
    print ("Listening on %s: net=%s, mask=%s, linktype=%d" % (dev, cap.getnet(), cap.getmask(), cap.datalink()))

    (header, payload) = cap.next()
    while header:
        print ('%s: captured %d bytes, truncated to %d bytes'
               % (datetime.datetime.now(), header.getlen(), header.getcaplen()))

        # TODO: Implement python-impacket in order to decode the captured packet and show his information

        (header, payload) = cap.next()


if __name__ == "__main__":
    main()
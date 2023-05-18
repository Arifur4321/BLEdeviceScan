import pyshark

# Set up the Wi-Fi sniffer
capture = pyshark.LiveCapture(interface='wlan1', display_filter='wlan.fc.type_subtype == 0x08 && wlan_mgt.tag_vendor_specific.oui == 0x001bc50f && wlan_mgt.tag.vendor_specific == 0x1e:16:fa:ff:0d:0d:12:00:5e:00')

# Start the Wi-Fi sniffing loop
for packet in capture.sniff_continuously():

    # Check if the packet is a Wi-Fi RID packet
    if 'RID' in packet.wlan_mgt.tag_vendor_specific:
        print('Wi-Fi RID packet:', packet)

        # Print out details of the Wi-Fi RID packet
        print('RID:', packet.wlan_mgt.tag_vendor_specific.RID)
        print('Version:', packet.wlan_mgt.tag_vendor_specific.Version)
        print('Device ID:', packet.wlan_mgt.tag_vendor_specific.DeviceID)
        print('Data:', packet.wlan_mgt.tag_vendor_specific.Data)
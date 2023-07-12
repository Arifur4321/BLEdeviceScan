import struct
import bluetooth._bluetooth as bluez

# Define the BLE device to scan
dev_id = 0

# Define the BLE socket
sock = bluez.hci_open_dev(dev_id)

# Set the filter to only receive advertising packets
hci_filter = bluez.hci_filter_new()
bluez.hci_filter_all_events(hci_filter)
bluez.hci_filter_set_ptype(hci_filter, bluez.HCI_EVENT_PKT)
bluez.hci_filter_set_event(hci_filter, bluez.EVT_LE_META_EVENT)
bluez.hci_filter_set_opcode(hci_filter, bluez.EVT_LE_META_EVENT)

# Start scanning for BLE devices
bluez.hci_send_cmd(sock, bluez.OGF_LE_CTL, bluez.OCF_LE_SET_SCAN_ENABLE, struct.pack("<BB", 0x01, 0x00))

# Continuously scan for BLE advertising packets
while True:
    # Get the next BLE event
    event = sock.recv(255)

    # Check if the event is an advertising packet
    if event[3] == bluez.EVT_LE_META_EVENT and event[4] == bluez.EVT_LE_ADVERTISING_REPORT:
        # Extract the advertising packet data
        data = event[6:]

        # Parse the advertising packet data
        message_counter = struct.unpack("<B", data[0:1])[0]
        message_type = struct.unpack("<B", data[1:2])[0]
        protocol_version = struct.unpack("<B", data[2:3])[0]
        operational_status = struct.unpack("<B", data[3:4])[0]
        height_type = struct.unpack("<B", data[4:5])[0]
        east_west_direction = struct.unpack("<B", data[5:6])[0]
        speed_multiplier = struct.unpack("<B", data[6:7])[0]
        direction = struct.unpack("<B", data[7:8])[0]
        speed = struct.unpack("<B", data[8:9])[0]
        vert_speed = struct.unpack("<B", data[9:10])[0]
        ua_latitude = struct.unpack("<i", data[10:14])[0] / 10**7
        ua_longitude = struct.unpack("<i", data[14:18])[0] / 10**7
        ua_pressure_altitude = struct.unpack("<i", data[18:22])[0] / 10
        ua_geodetic_altitude = struct.unpack("<i", data[22:26])[0] / 10
        ua_height_agl = struct.unpack("<i", data[26:30])[0] / 10
        horizontal_accuracy = struct.unpack("<B", data[30:31])[0]
        vertical_accuracy = struct.unpack("<B", data[31:32])[0]
        baro_accuracy = struct.unpack("<B", data[32:33])[0]
        speed_accuracy = struct.unpack("<B", data[33:34])[0]
        timestamp = struct.unpack("<I", data[34:38])[0]
        reserved = struct.unpack("<B", data[38:39])[0]
        timestamp_accuracy = struct.unpack("<B", data[39:40])[0]

        # Print out the advertising packet data
        print("Message Counter:", message_counter)
        print("Message Type:", message_type)
        print("Protocol Version:", protocol_version)
        print("Operational Status:", operational_status)
        print("Height Type:", height_type)
        print("East/West Direction Segment:", east_west_direction)
        print("Speed Multiplier:", speed_multiplier)
        print("Direction:", direction)
        print("Speed:", speed)
        print("Vert Speed:", vert_speed)
        print("UA Latitude:", ua_latitude)
        print("UA Longitude:", ua_longitude)
        print("UA Pressure Altitude:", ua_pressure_altitude)
        print("UA Geodetic Altitude:", ua_geode
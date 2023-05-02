from bluepy.btle import Scanner, DefaultDelegate
import gpsd

# Connect to the GPS module
gpsd.connect()

# Define a delegate class for BLE scanning
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device {dev.addr}")
                        # Check if the device is an Aerobits IDME Pro device
            value_text = dev.getValueText(9)
            print("dev.getValueText(9) :", value_text)
            if value_text is not None and "IDME" in value_text:
                # Connect to the device
                print(f"Connecting to IDME Pro device {dev.addr}")
                idme_device = dev.connect()

                # Get the GPS data
                try:
                    gps_data = gpsd.get_current()
                    if gps_data.mode >= 2:
                        latitude = gps_data.lat
                        longitude = gps_data.lon
                        print(f"IDME Pro device {dev.addr} location: ({latitude}, {longitude})")
                    else:
                        print(f"IDME Pro device {dev.addr} location: Unknown")
                except Exception as e:
                    print(f"Error getting GPS data for IDME Pro device {dev.addr}: {e}")

                # Disconnect from the device
                idme_device.disconnect()

            # Check if the device is a GPS device
            elif "GPS" in value_text:
                # Connect to the device
                print(f"Connecting to GPS device {dev.addr}")
                gps_device = dev.connect()

                # Get the GPS data
                try:
                    gps_data = gpsd.get_current()
                    if gps_data.mode >= 2:
                        latitude = gps_data.lat
                        longitude = gps_data.lon
                        print(f"GPS device {dev.addr} location: ({latitude}, {longitude})")
                    else:
                        print(f"GPS device {dev.addr} location: Unknown")
                except Exception as e:
                    print(f"Error getting GPS data for GPS device {dev.addr}: {e}")

                # Disconnect from the device
                gps_device.disconnect()
        elif isNewData:
            print(f"Received new data from device {dev.addr}")

            # Check if the device is an Aerobits IDME Pro device
            value_text = dev.getValueText(9)
            print("dev.getValueText(9) :", value_text)
            if value_text is not None and "IDME" in value_text:
                # Connect to the device
                print(f"Connecting to IDME Pro device {dev.addr}")
                idme_device = dev.connect()

                # Get the GPS data
                try:
                    gps_data = gpsd.get_current()
                    if gps_data.mode >= 2:
                        latitude = gps_data.lat
                        longitude = gps_data.lon
                        print(f"IDME Pro device {dev.addr} location: ({latitude}, {longitude})")
                    else:
                        print(f"IDME Pro device {dev.addr} location: Unknown")
                except Exception as e:
                    print(f"Error getting GPS data for IDME Pro device {dev.addr}: {e}")

                # Disconnect from the device
                idme_device.disconnect()

            # Check if the device is a GPS device
            elif "GPS" in value_text:
                # Connect to the device
                print(f"Connecting to GPS device {dev.addr}")
                gps_device = dev.connect()

                # Get the GPS data
                try:
                    gps_data = gpsd.get_current()
                    if gps_data.mode >= 2:
                        latitude = gps_data.lat
                        longitude = gps_data.lon
                        print(f"GPS device {dev.addr} location: ({latitude}, {longitude})")
                    else:
                        print(f"GPS device {dev.addr} location: Unknown")
                except Exception as e:
                    print(f"Error getting GPS data for GPS device {dev.addr}: {e}")

                # Disconnect from the device
                gps_device.disconnect()

# Scan for BLE devices
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(2.0)
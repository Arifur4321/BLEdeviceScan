from bluepy.btle import Scanner, DefaultDelegate, ScanEntry
import math

# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev: ScanEntry, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)
            # Estimate the distance based on the RSSI value
            distance = self.estimateDistance(dev.rssi)
            print("  Estimated distance:", distance, "meters")
        elif isNewData:
            print("Received new data from device:", dev.addr)
            # Estimate the distance based on the RSSI value
            print("  RSSI:", dev.rssi)
            distance = self.estimateDistance(dev.rssi)
            print("  Estimated distance:", distance, "meters")

        # Extract latitude and longitude information from advertising packets
        for (adtype, desc, value) in dev.getScanData():
            # Check if the manufacturer data is for iBeacon
                    uuid = value[8:40]
                    try :
                        major = int(value[40:44], 16)
                        minor = int(value[44:48], 16)

                    except ValueError:
                        # Handle the case where the substring is not a valid hexadecimal value
                        major = 0  # Set a default value    
                        minor = 0  
                    try:
                        tx_power = int(value[48:50], 16) - 256
                    except ValueError:
                     # Handle the case where the substring is not a valid hexadecimal value
                        tx_power = -59
                    rssi = dev.rssi
                    distance = self.estimateDistance(rssi, tx_power)
                    lat, lon = self.getLatLon(uuid, major, minor)
                    print("  Latitude:", lat)
                    print("  Longitude:", lon)

    def estimateDistance(self, rssi, tx_power=-59):
        # Calculate the distance based on the RSSI value using the log-distance path loss model
        # The constants used in this formula are based on empirical measurements and can vary depending on the environment
        n = 2.0  # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
        return math.pow(10, (tx_power - rssi) / (10 * n))

    def getLatLon(self, uuid, major, minor):
        # Calculate the latitude and longitude based on the iBeacon UUID, major, and minor values
        # The latitude and longitude values are encoded in the iBeacon UUID and can be decoded using the following formula
        # lat = (UUID[9] * 256 + UUID[10]) / 90.0
        # lon = (UUID[11] * 256 + UUID[12]) / 180.0
        lat = (int(uuid[18:20], 16) * 256 + int(uuid[20:22], 16)) / 90.0
        lon = (int(uuid[22:24], 16) * 256 + int(uuid[24:26], 16)) / 180.0
        return lat, lon

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their device address, name, RSSI, estimated distance, latitude, and longitude
devices = scanner.scan(10.0)
for dev in devices:
    print("Device address:", dev.addr)
    print("  Device name:", dev.getValueText(9))
    print("  RSSI:", dev.rssi)
    # Estimate the distance based on the RSSI value
    distance = ScanDelegate().estimateDistance(dev.rssi)
    print("  Estimated distance:", distance, "meters")

    print("  Advertising data:")
    for (adtype, desc, value) in dev.getScanData():
        print("    %s: %s" % (desc, value))
 
    # Extract latitude and longitude information from advertising packets
    for (adtype, desc, value) in dev.getScanData():
           # Check if the manufacturer data is for iBeacon
                uuid = value[8:40]
                try :
                        major = int(value[40:44], 16)
                        minor = int(value[44:48], 16)

                except ValueError:
                        # Handle the case where the substring is not a valid hexadecimal value
                        major = 0  # Set a default value    
                        minor = 0 
                try:
                   tx_power = int(value[48:50], 16) - 256
                except ValueError:
                 # Handle the case where the substring is not a valid hexadecimal value
                   tx_power = -59
                rssi = dev.rssi
                distance = ScanDelegate().estimateDistance(rssi, tx_power)
                lat, lon = ScanDelegate().getLatLon(uuid, major, minor)
                print("  Latitude:", lat)
                print("  Longitude:", lon)
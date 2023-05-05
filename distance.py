import requests
import json
import struct
import asyncio
import math
import time
import aioblescan as aiobs
from bleparser import BleParser
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError

# Google Maps Geolocation API endpoint and API key
GEOLOCATION_API_URL = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBqyGDMUcp4FZPGL6XICmX9ImxYzpIH99M"

# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device: {dev.addr}")
            print(f"  Device name: {dev.getValueText(9)}")
            print(f"  RSSI: {dev.rssi}")
            # Estimate the distance based on the RSSI value
            distance = self.estimateDistance(dev.rssi)
            print(f"  Estimated distance: {distance:.2f} meters")
            lat, lon = self.getLocation(dev.addr)
            print(f"  Latitude: {lat}")
            print(f"  Longitude: {lon}")
            print("  Advertising data:")
            self.parseAdvertisingData(dev)

        elif isNewData:
            print(f"Received new data from device: {dev.addr}")
            print("  Advertising data:")
            self.parseAdvertisingData(dev)

    def estimateDistance(self, rssi):
        # Calculate the distance based on the RSSI value using the log-distance path loss model
        # The constants used in this formula are based on empirical measurements and can vary depending on the environment
        txPower = -59 # The transmit power of the BLE device in dBm
        n = 2.0 # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
        return math.pow(10, (txPower - rssi) / (10 * n))

    def getLocation(self, mac_address):
        # Scan for Wi-Fi access points and get their MAC addresses and signal strengths
        wifi_access_points = []
        wifi_scanner = Scanner()
        wifi_devices = wifi_scanner.scan(5.0)
        for wifi_device in wifi_devices:
            for (adtype, desc, value) in wifi_device.getScanData():
                if desc == "Complete Local Name" and value == mac_address:
                    wifi_access_points.append({
                        "macAddress": wifi_device.addr.replace(":", ""),
                        "signalStrength": wifi_device.rssi
                    })

        # Send a POST request to the Google Maps Geolocation API with the Wi-Fi access points and cell towers
        data = {
            "wifiAccessPoints": wifi_access_points
        }
        response = requests.post(GEOLOCATION_API_URL, data=json.dumps(data))

        # Parse the response and return the latitude and longitude
        if response.status_code == 200:
            location = response.json()["location"]
            return location["lat"], location["lng"]
        else:
            return None, None

    def parseAdvertisingData(self, dev):
        for (adtype, desc, value) in dev.getScanData():
            print(f"    {desc}: {value}")
            parser = BleParser(discovery=False, filter_duplicates=True)

        
            sensor_data, tracker_data = parser.parse_raw_data(value)

            if tracker_data:
                print("  Tracker data:", tracker_data)

            if sensor_data:
                print("  Sensor data:", sensor_data)

  
 
 

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Continuously scan for Bluetooth devices and print out their information
while True:
    try:
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
                #data = bytes(bytearray.fromhex(value))
             

      
    

            lat, lon =  ScanDelegate().getLocation(dev.addr)
            print("  Latitude:", lat)
            print("  Longitude:", lon)
         
                 
    except BTLEDisconnectError:
        print("Device disconnected")
    time.sleep(10)  # Delay for 10 seconds before scanning again
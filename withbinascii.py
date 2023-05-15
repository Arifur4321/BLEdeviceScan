import requests
import json
from bluepy.btle import Scanner, DefaultDelegate
import math 
from pymodes import decoders

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            # Add the MAC address of the device to a list of nearby MAC addresses
            nearby_macs.append(dev.addr)
        elif isNewData:
            print("Received new data from device:", dev.addr)
            # Check if the received data is an ASTM F3411 / ASD-STAN 4709-002 UAV direct remote identification signal
            
            data = bytes.fromhex(dev.getValueText(255))
            decoded_data = decoders.uav_direct_remote_id(data)
            print("Decoded UAV direct remote identification signal from device:", dev.addr)
            print("Decoded UAV data:",decoded_data)
                

    def estimateDistance(self, rssi):
        # Calculate the distance based on the RSSI value using the log-distance path loss model
        # The constants used in this formula are based on empirical measurements and can vary depending on the environment
        txPower = -59 # The transmit power of the BLE device in dBm
        n = 2.0 # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
        return math.pow(10, (txPower - rssi) / (10 * n))

# Create a scanner object and set the delegate to handle incoming advertisements
scanner = Scanner().withDelegate(ScanDelegate())

# Initialize a list to store the MAC addresses of nearby devices
nearby_macs = []

while True:
    # Scan for BLE devices for 10 seconds
    devices = scanner.scan(10.0)

    # Print information about each discovered device
    for dev in devices:
        distance = ScanDelegate().estimateDistance(dev.rssi)
        print("  Estimated distance:", distance, "meters")
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))

    # Send a POST request to the Google Maps Geolocation API with the MAC addresses of nearby devices
    if nearby_macs:
        print ("nearby mac :",nearby_macs)
        url = "https://www.googleapis.com/geolocation/v1/geolocate?key=YOUR_API_KEY"
        data = {
            "considerIp": "false",
            "wifiAccessPoints": [{"macAddress": mac} for mac in nearby_macs]
        }
        print ("data :",data)

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print ("response from apikey:",response)
        if response.status_code == 200:
            location = response.json()["location"]
            print("Estimated location:", location["lat"], location["lng"])
        else:
            print("Error:", response.status_code, response.text)

    # Clear the list of nearby MAC addresses for the next scan
    nearby_macs = []
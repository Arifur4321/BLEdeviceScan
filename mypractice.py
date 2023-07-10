from bluepy import btle
import binascii
import struct

# Define the Open Drone ID service UUID
ODID_SERVICE_UUID = "00020001-0000-1000-8000-00805F9B34FB"

class ODIDScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovering:")
               
        if isNewData:
            for (adtype, desc, value) in dev.getScanData():
                if adtype == 22 and desc == "16b Service Data":
                    print(" opendroneid:", dev.addr)

                    service_data = binascii.unhexlify(value)
                    decode_service_data(service_data)

def decode_service_data(service_data):
    # Example decoding logic
    # Modify this based on the actual structure and format of the service data

    message_type = service_data[0]
    operator_id = service_data[1:9]
    location_latitude = struct.unpack('!d', service_data[9:17])[0]
    location_longitude = struct.unpack('!d', service_data[17:25])[0]
    height = struct.unpack('!f', service_data[25:29])[0]
#    altitude_pressure = struct.unpack('!f', service_data[29:33])[0]
#    altitude_pressure = struct.unpack('!H', service_data[29:31])[0]

    print("Message Type:", message_type)
    print("Operator ID:", operator_id)
    print("Location Latitude:", location_latitude)
    print("Location Longitude:", location_longitude)
    print("Height:", height)
#    print("Altitude Pressure:", altitude_pressure)
    print()

# Create a scanner object and set the delegate
scanner = btle.Scanner().withDelegate(ODIDScanDelegate())

while True:
    devices = scanner.scan(timeout=10)

    # Print the scanned devices and their service data
    for dev in devices:
        # print("Device:", dev.addr)
        for (adtype, desc, value) in dev.getScanData():
            if adtype == 22 and desc == "16b Service Data":
                print("opendroneid :", dev.addr)
 
                service_data = binascii.unhexlify(value)
                decode_service_data(service_data)
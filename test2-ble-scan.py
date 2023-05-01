import msgpack
from bluepy.btle import Scanner, DefaultDelegate, UUID
import binascii
# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)

             

        elif isNewData:
            print("Received new data from device:", dev.addr)
            
             # Parse Aerobits IDME Pro advertising data
            # Parse Aerobits IDME Pro advertising data
        ad = dev.getScanData()
        for (adtype, desc, value) in ad:
            if adtype == 22 and value.startswith(b'\xfa\xff\x0d\x1c'.decode()):
                altitude = int.from_bytes(value[7:9], byteorder='big', signed=True) * 0.1
                latitude = int.from_bytes(value[9:13], byteorder='big', signed=True) * 0.0001
                longitude = int.from_bytes(value[13:17], byteorder='big', signed=True) * 0.0001
                distance = int.from_bytes(value[17:19], byteorder='big', signed=True) * 0.1
                print("Decoded data:")
                print("  Altitude:", altitude)
                print("  Latitude:", latitude)
                print("  Longitude:", longitude)
                print("  Distance:", distance)



            service_data = None
            for (adtype, desc, value) in dev.getScanData():
                if adtype == 22 and desc.startswith('16b Service Data'):
                    service_data = value
                    break

            if service_data is not None:
                # Parse the Service Data
                uuid = binascii.unhexlify(service_data[0:4])[::-1]  # reverse byte order
                data = binascii.unhexlify(service_data[4:])

                # Print the parsed data
                print("Service UUID:", binascii.hexlify(uuid))
                print("Data:", binascii.hexlify(data))

            # Decode MessagePack data
            for (adtype, desc, value) in dev.getScanData():
                if adtype == 255:  # Manufacturer Specific Data
                    if value.startswith(b'\x1d\xa5\x94\x01'):  # Aerobits IDME Pro
                        data = msgpack.unpackb(value[4:])
                        print("Decoded data:", data)
                        print("Altitude:", data['altitude'])
                        print("Latitude:", data['latitude'])
                        print("Longitude:", data['longitude'])
                        print("Distance:", data['distance'])
            
            service_data = dev.getValueText(22)
            
            if service_data is not None and service_data.startswith('16b'):
                # Extract the raw bytes from the service data string
                raw_data = binascii.unhexlify(service_data[6:])

             
# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their advertising data
devices = scanner.scan(10.0)
for dev in devices:
    print("Device address:", dev.addr)
    print("  Device name:", dev.getValueText(9))
    print("  RSSI:", dev.rssi)
    print("  Advertising data:")
    for (adtype, desc, value) in dev.getScanData():
        print("    %s: %s" % (desc, value))

        if desc.startswith('16b'):

            print ("  raw decode data > ",  value)
             
            # Parse Aerobits IDME Pro advertising data
    ad = dev.getScanData()
    for (adtype, desc, value) in ad:
        if adtype == 22 and value.startswith(b'\xfa\xff\x0d\x1c'.decode()):
            altitude = int.from_bytes(value[7:9], byteorder='big', signed=True) * 0.1
            latitude = int.from_bytes(value[9:13], byteorder='big', signed=True) * 0.0001
            longitude = int.from_bytes(value[13:17], byteorder='big', signed=True) * 0.0001
            distance = int.from_bytes(value[17:19], byteorder='big', signed=True) * 0.1
            print("Decoded data:")
            print("  Altitude:", altitude)
            print("  Latitude:", latitude)
            print("  Longitude:", longitude)
            print("  Distance:", distance)
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, UUID
import math

# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
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
            distance = ScanDelegate().estimateDistance(dev.rssi)

            print("  Estimated distance:", distance, "meters")

                
            print("  Advertising data:")
            for (adtype, desc, value) in dev.getScanData():
                print("    %s: %s" % (desc, value))
                
                mac_address = dev.addr

                    # Connect to the Aerobits IDME Pro device and get the UA ID Type and UAS ID
                device = Peripheral(mac_address, addrType="public")
                device.connect("public", "fast")
                service_uuid = UUID("0000fff0-0000-1000-8000-00805f9b34fb")
                ua_id_type_uuid = UUID("0000fff1-0000-1000-8000-00805f9b34fb")
                uas_id_uuid = UUID("0000fff2-0000-1000-8000-00805f9b34fb")
                service = device.getServiceByUUID(service_uuid)
                ua_id_type_char = service.getCharacteristics(ua_id_type_uuid)[0]
                uas_id_char = service.getCharacteristics(uas_id_uuid)[0]
                ua_id_type = ua_id_type_char.read().decode('utf-8')
                uas_id = uas_id_char.read().decode('utf-8')
                print("UA ID Type:", ua_id_type)
                print("UAS ID:", uas_id)

    def estimateDistance(self, rssi):
        # Calculate the distance based on the RSSI value using the log-distance path loss model
        # The constants used in this formula are based on empirical measurements and can vary depending on the environment
        txPower = -59 # The transmit power of the BLE device in dBm
        n = 2.0 # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
        return math.pow(10, (txPower - rssi) / (10 * n))

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their device address, name, RSSI, and estimated distance
devices = scanner.scan(100.0)
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
         
        mac_address = dev.addr

            # Connect to the Aerobits IDME Pro device and get the UA ID Type and UAS ID
        device = Peripheral(mac_address, addrType="public")
        device.connect("public", "fast")
        service_uuid = UUID("0000fff0-0000-1000-8000-00805f9b34fb")
        ua_id_type_uuid = UUID("0000fff1-0000-1000-8000-00805f9b34fb")
        uas_id_uuid = UUID("0000fff2-0000-1000-8000-00805f9b34fb")
        service = device.getServiceByUUID(service_uuid)
        ua_id_type_char = service.getCharacteristics(ua_id_type_uuid)[0]
        uas_id_char = service.getCharacteristics(uas_id_uuid)[0]
        ua_id_type = ua_id_type_char.read().decode('utf-8')
        uas_id = uas_id_char.read().decode('utf-8')
        print("UA ID Type:", ua_id_type)
        print("UAS ID:", uas_id)
from bluepy.btle import Scanner, Peripheral, UUID

# Define the UUIDs for the IDME PRO service and characteristic
service_uuid = UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
characteristic_uuid = UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e")

# Define the timeout for the Bluetooth LE scan (in seconds)
scan_timeout = 1000

# Scan for nearby devices with the IDME PRO service UUID
scanner = Scanner()
devices = scanner.scan(scan_timeout)

idme_pro_macs = []

for device in devices:
    for (adtype, desc, value) in device.getScanData():
        if desc == "Complete Local Name" and value == "IDME PRO":
            for service in device.getScanData():
                if service[2].lower() == str(service_uuid).lower():
                    idme_pro_macs.append(device.addr)

# Loop through each IDME PRO device and read data from its characteristic
for device_mac in idme_pro_macs:
    try:
        # Connect to the IDME PRO
        peripheral = Peripheral(device_mac)

        # Get the IDME PRO service and characteristic
        service = peripheral.getServiceByUUID(service_uuid)
        characteristic = service.getCharacteristics(characteristic_uuid)[0]

        # Read the IDME PRO data from the characteristic
        idme_pro_data = characteristic.read()

        # Do something with the IDME PRO data
        print(f"IDME PRO data received from {device_mac}:")
        print(idme_pro_data)

        # Disconnect from the IDME PRO
        peripheral.disconnect()

    except Exception as e:
        print(f"Failed to connect to {device_mac}: {e}")

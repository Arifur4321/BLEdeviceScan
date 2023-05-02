from bluepy.btle import Peripheral, DefaultDelegate

class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("Received data: ", data.decode("utf-8"))

device_address = "7C:DF:A1:5A:4B:1E" # replace with the MAC address of your IDME Pro device
device = Peripheral(device_address)

advertising_data_uuid = "0000fff4-0000-1000-8000-00805f9b34fb" # replace with the UUID of the advertising data characteristic
advertising_data_characteristic = device.getCharacteristics(uuid=advertising_data_uuid)[0]
advertising_data_handle = advertising_data_characteristic.getHandle()
device.writeCharacteristic(advertising_data_handle + 1, b"\x01\x00")

device.withDelegate(NotificationDelegate())

while True:
    if device.waitForNotifications(1.0):
        continue
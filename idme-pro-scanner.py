               
from bleparser import BleParser

data_string = "faff0d7d12200701005cbe0a182732cd0ab9075d08f4074a63d98b0100"
data = bytes(bytearray.fromhex(data_string))

ble_parser = BleParser()
sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)
print(sensor_msg)
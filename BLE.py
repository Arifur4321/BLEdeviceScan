from bleparser import BleParser

data_string = "043e2502010000219335342d5819020106151695fe5020aa01da219335342d580d1004fe004802c4"
data = bytes(bytearray.fromhex(data_string))

ble_parser = BleParser()
sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)
print(sensor_msg)
from bleparser import BleParser
import struct




def decode_service_data(service_data):
    # Unpack the service data into its component parts
    temperature, humidity, light, battery, pressure, co2 = struct.unpack('<hhhhhh', service_data[4:])

    # Convert the values to their respective units
    temperature = temperature / 100.0
    humidity = humidity / 100.0
    light = light / 100.0
    battery = battery / 1000.0
    pressure = pressure / 100.0
    co2 = co2 / 10.0

    # Return the decoded values as a dictionary
    return {
        'temperature': temperature,
        'humidity': humidity,
        'light': light,
        'battery': battery,
        'pressure': pressure,
        'co2': co2
    }

if __name__ == '__main__':
    # Example service data
    service_data = b'\xfa\xff\r}\x12 \x07\x01\x00\\\xbe\n\x182s-\xd0\xab\x90u\xd0\x8f@t\xa6=\x98\xb0\x10\x00'

    # Decode the service data   or  043e2502010000219335342d5819020106151695fe5020aa01da219335342d580d1004fe004802c4
    data_string = "faff0d7d12200701005cbe0a182732cd0ab9075d08f4074a63d98b0100"
    data = bytes(bytearray.fromhex(data_string))
    print ("data" ,data)
    ble_parser = BleParser()
    sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)
    print(sensor_msg)
    decoded_data = decode_service_data(data)

    # Print the decoded values
    print('Temperature: {:.2f} C'.format(decoded_data['temperature']))
    print('Humidity: {:.2f} %'.format(decoded_data['humidity']))
    print('Light: {:.2f} lux'.format(decoded_data['light']))
    print('Battery: {:.2f} V'.format(decoded_data['battery']))
    print('Pressure: {:.2f} hPa'.format(decoded_data['pressure']))
    print('CO2: {:.1f} ppm'.format(decoded_data['co2']))
import msgpack
from bluedot import scanner, UID

def print_temperature_and_pressure_values(device_id, temperature, pressure, altitude=None):
    print(f"\nTemperature and Pressure values received from {device_id}:")
    if altitude is not None:
        print("\tAltitude:\t{}\t{}".format(*altitude))
    else:
        print("\tAltitude: Not available.")
    print("\tTemperature: {}\t{}".format(*temperature))
    print("\tPressure: {}".format(*pressure))

def on_data_available(connection_handle, scan_record):
    global device_id
    message = scan_record.message.split("\x00")[-1].decode()
    data = msgpack.loads(message)
    
    temperature = data["temperature"]
    pressure = data["pressure"]
    
    if "altitude" in data:
        altitude = data["altitude"]
        
        # Printing decoded tempertaure and pressue values here
        print_temperature_and_pressure_values(str(device_id), temperature, pressure, altitude)

device_id = str(int(time.time()))   # Unique identifier for each run of this program
global_settings = {"name": "\u30C6"}    # Sets manufacturer specific global settings
profile = scanner.ProfileFilter("Custom Filter Profile", serviceUUIDs=[uid], characteristicsUUIDs=[
... '00000fff0-00000-1000-8000-00805f9b34fb8'] + serviceUUIDs, reportCharacteristics=['00000ffff-00000-1000-8000-00805f9b34fb8'], **serviceUUIDs, **characteristicsUUIDs, **global_settings)
filtered = scanner.ServicesFilter('aerobit')
discoverer = scanner.BaseDiscoveryOptions(['public', 'randomize_adv_filters'], 'discover_inq')
proximity = [scanner.GAPRoleParameters('client'), 'any', [], False]
options = {'timeout': 10}
scanner = scanner.Scanner(device='hci0', discoverer=discoverer, options=options, services_filter=filtered, profiles=[profile], proximity=proximity, signal=-75)
print("Start searching!")

while True:
    try:
        device = next(scanner.start_scan(blocking=True))
        connection = device['connection']
        connection.on_data_available.add_done_callback(lambda x : print("Done"))
        connection.on_data_available.add_signal_listener(lambda x: print("Signal: "+`
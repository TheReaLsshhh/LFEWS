from pymodbus.client import ModbusTcpClient
from celery import shared_task
from django.apps import apps  # Ensures models are loaded dynamically

@shared_task
def store_modbus_data():
    Bywntest = apps.get_model('app1', 'Bywntest')
    Canalumtest = apps.get_model('app1', 'Canalumtest')
    Kalumbuyantest = apps.get_model('app1', 'Kalumbuyantest')
    Jugnotest = apps.get_model('app1', 'Jugnotest')

    modbus_devices = [
        {"ip": "192.168.41.12", "model": Kalumbuyantest},
        {"ip": "192.168.41.13", "model": Canalumtest},
        {"ip": "192.168.41.10", "model": Bywntest},
        {"ip": "192.168.41.18", "model": Jugnotest},
    ]

    results = {}

    for device in modbus_devices:
        client = ModbusTcpClient(device["ip"], port=100)

        try:
            if not client.connect():
                raise ConnectionError(f"Could not connect to Modbus server at {device['ip']}")

            result = client.read_holding_registers(address=6, count=1)

            if result.isError() or result.registers is None:
                print(f"No response from {device['ip']}, storing 0 in database.")
                data_value_cm = 0
            else:
                data_value_mm = result.registers[0]  # Data in millimeters
                data_value_cm = data_value_mm / 10  # Convert mm to cm

            # Save data to respective model
            device["model"].objects.create(data=data_value_cm)
            results[device["ip"]] = f"Data saved: {data_value_cm} cm"

        except Exception as e:
            print(f"Error with {device['ip']}: {e}")
            device["model"].objects.create(data=0)  # Store 0 in case of an error
            results[device["ip"]] = f"Error, stored 0 in database: {e}"

        finally:
            client.close()

    return results


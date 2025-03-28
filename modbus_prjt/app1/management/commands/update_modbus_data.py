from celery import shared_task
from pymodbus.client import ModbusTcpClient
from app1.models import Bywntest

@shared_task
def store_modbus_data():
    client = ModbusTcpClient('192.168.41.13', port=100)

    try:
        # Attempt connection
        connection = client.connect()
        if not connection:
            print("Connection to Modbus server failed")
            return "Connection to Modbus server failed"

        # Read data from Modbus (assuming register 6)
        result = client.read_holding_registers(6, 1)  # Register 6, 1 count
        if result.isError():
            print(f"Error reading Modbus register: {result}")
            return f"Error reading Modbus register: {result}"
        else:
            data_value = result.registers[0]  # Get the first (and only) register value
            print(f"Data at register 6: {data_value}")

            # Save data to the database
            Bywntest.objects.create(data=data_value)
            print("Data saved to database")
            return f"Data saved: {data_value}"

    except Exception as e:
        print(f"Error during polling or database update: {e}")
        return f"Exception occurred: {e}"

    finally:
        client.close()
        print("Connection closed")

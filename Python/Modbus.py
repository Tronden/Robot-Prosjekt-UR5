from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform

# Create an instance of ModbusServer
server = ModbusServer("158.38.140.101", 502, no_block=True)

try:
    print("Start server...")
    server.start()
    print("Server is online")

    # Initialize the state for each joint register
    state = [0] * 6  # Six registers for six joints

    while True:
        # Read and check current state of registers 0-5
        for i in range(6):
            current_value = server.data_bank.get_holding_registers(i)
            if current_value is not None:
                # Normalize the values to handle positive and negative ranges
                normalized_value = current_value[0] if current_value[0] <= 32767 else current_value[0] - 65536

                # Check if the retrieved state has changed
                if state[i] != normalized_value:
                    state[i] = normalized_value

        print(f"Angles = {state[0], state[1], state[2], state[3], state[4], state[5]}")
        sleep(0.5)

except Exception as e:
    print(f"An error occurred: {e}")
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")
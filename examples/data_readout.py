# Import required modules
import asyncio
from triki import TRIKIController
from triki import TRIKIScanner

DEVICE_BT_ADDRESS = "AA:BB:CC:DD:EE:FF"

async def main():
    print("Searching for devices...")

    # Create scanner
    scanner = TRIKIScanner()
    # Scan for TRIKI controllers
    await scanner.scan()
    # Get scanned TRIKI controllers
    scanned_devices = scanner.scanned_devices
    # Check if devices weren't found
    if len(scanned_devices) == 0:
        print("No devices found.")
        return

    # Set the BT address from the first device
    device_bt_address = scanned_devices[0].address
    # Create TRIKI controller object
    device = TRIKIController(device_bt_address)
    print(f"Connecting to device ({device_bt_address})")
    # Connect to the TRIKI controller
    await device.connect()
    # Check if connection was successful
    if device.is_connected:
        print("Connected!")
    else:
        print("Failed to connect!")
        return

    # Loop this until user exits the program or device disconnects
    try:
        while device.is_connected:
            print(f"Battery level: {device.battery_level}%") # Battery level
            print(f"FW Version: {device.firmware_version}")  # FW version
            # GYRO
            print(f"Spin X: {device.spin_x}", end=" | ") # X spin
            print(f"Spin Y: {device.spin_y}", end=" | ") # Y spin
            print(f"Turn Z: {device.turn_z}", end=" | ") # Z turn
            # ACCEL
            print(f"Tilt X: {device.tilt_x}", end=" | ") # X tilt
            print(f"Tilt Y: {device.tilt_y}", end=" | ") # Y tilt
            print(f"Flip Z: {device.flip_z}", end=" | ") # Z flip

            print(f"Button: {device.button_pressed}") # Button
            await asyncio.sleep(0.1)
    finally:
        # Disconnect from the TRIKI controller
        await device.disconnect()



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")

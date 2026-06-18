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
            # Turn on LED
            await device.toggle_led(True)
            await asyncio.sleep(1)
            # Turn off LED
            await device.toggle_led(False)
            await asyncio.sleep(1)
    finally:
        # Disconnect from the TRIKI controller
        await device.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")

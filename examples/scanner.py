# Import required modules
import asyncio
from triki import TRIKIScanner

# Create scanner
scanner = TRIKIScanner()

async def main():
    print("Scanning for devices...")
    # Scan for TRIKI controllers
    await scanner.scan()
    print("Found devices:")
    # Print scanned devices
    for device in scanner.scanned_devices:
        print(f"{device.name}   {device.address}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")
from bleak import BleakScanner, BLEDevice
from .types import TRIKIDevice


class TRIKIScanner:
    """Base class for the TRIKI controller scanner"""
    __scanner = None
    __bleak_devices: list[BLEDevice] = []
    __scanned_devices: list[TRIKIDevice] = []

    def __init__(self) -> None:
        self.__scanner = BleakScanner()

    async def scan(self) -> None:
        """Scan for TRIKI controllers"""
        self.__bleak_devices = await self.__scanner.discover()
        self.__scanned_devices.clear()

        for device in self.__bleak_devices:
            if device.name is not None and "Triki" in device.name:
                triki_device = TRIKIDevice("Triki " + device.address[-6:], device.address)
                self.__scanned_devices.append(triki_device)

    @property
    def scanned_devices(self) -> list[TRIKIDevice]:
        """Scanned TRIKI controllers"""
        return self.__scanned_devices

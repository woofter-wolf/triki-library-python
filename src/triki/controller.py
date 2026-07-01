import bleak.exc
from bleak import BleakClient

from .exceptions import TRIKIDeviceNotFoundError, TRIKINotConnectedError, TRIKIConnectionError

UART_RX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
BATTERY_LEVEL_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
FIRMWARE_VERSION_UUID = "00002a26-0000-1000-8000-00805f9b34fb";
LED_CHARACTERISTIC_UUID = "6e400004-b5a3-f393-e0a9-e50e24dcca9e"
START_STREAM_COMMAND = bytes.fromhex("20 10 00 d0 07 34 00 03")


class TRIKIController:
    """
    Base class for the TRIKI controller

    Args:
        address:
            Device Bluetooth address
    """
    __device_client: BleakClient = None
    __bt_address: str = "AA:BB:CC:DD:EE:FF"

    __battery_level: int = 0
    __firmware_version: str = ""
    __sensor_spin_x: int = 0
    __sensor_spin_y: int = 0
    __sensor_turn_z: int = 0
    __sensor_tilt_x: int = 0
    __sensor_tilt_y: int = 0
    __sensor_flip_z: int = 0
    __button_pressed: bool = False

    def __init__(self, address: str) -> None:
        self.__bt_address = address

    def __little_endian(self, a: int, b: int) -> int:
        """Parse data by using a little endian algorithm"""
        x = a + (b * 256)
        if x > 32767:
            x -= 65536
        return x

    def __parse_received_data(self, sender, data: bytearray) -> None:
        """Parse data when received"""
        if len(data) >= 16 and data[0] == 0x22:
            data_sliced = data.hex(" ").split(" ")
            data_decimal = []
            for i in range(len(data_sliced)):
                data_decimal.append(int(data_sliced[i], 16))

            self.__sensor_spin_x = self.__little_endian(data_decimal[2], data_decimal[3])
            self.__sensor_spin_y = self.__little_endian(data_decimal[4], data_decimal[5])
            self.__sensor_turn_z = self.__little_endian(data_decimal[6], data_decimal[7])
            self.__sensor_tilt_x = self.__little_endian(data_decimal[8], data_decimal[9])
            self.__sensor_tilt_y = self.__little_endian(data_decimal[10], data_decimal[11])
            self.__sensor_flip_z = self.__little_endian(data_decimal[12], data_decimal[13])

            self.__button_pressed = data_decimal[15] == 1

    async def connect(self, raise_exception_on_fail: bool = False) -> None:
        """Connect to the TRIKI controller"""
        self.__device_client = BleakClient(self.__bt_address, timeout=10)
        try:
            await self.__device_client.connect()
        except bleak.exc.BleakDeviceNotFoundError as error:
            if raise_exception_on_fail:
                raise TRIKIDeviceNotFoundError(
                    f"TRIKI device with address {self.__bt_address} was not found"
                ) from error
        except bleak.exc.BleakError as error:
            if raise_exception_on_fail:
                raise TRIKIConnectionError(
                    f"Connection with TRIKI device (at {self.__bt_address}) failed"
                ) from error

        if self.__device_client.is_connected:
            try:
                battery_data = await self.__device_client.read_gatt_char(BATTERY_LEVEL_UUID)
                self.__battery_level = int(battery_data[0])

                firmware_data = await self.__device_client.read_gatt_char(FIRMWARE_VERSION_UUID)
                self.__firmware_version = firmware_data.decode("utf-8").strip("\x00")

                await self.__device_client.start_notify(UART_TX_UUID, self.__parse_received_data)

                await self.__device_client.write_gatt_char(
                    UART_RX_UUID, START_STREAM_COMMAND, response=True
                )
            except bleak.exc.BleakError as error:
                raise TRIKIConnectionError(
                    f"Connected to the TRIKI device (at {self.__bt_address}), but initialization failed"
                ) from error
        else:
            raise TRIKIConnectionError(
                f"Connection with TRIKI device (at {self.__bt_address}) failed"
            )

    async def disconnect(self) -> None:
        """Disconnect from the TRIKI device"""
        if self.__device_client is not None and self.__device_client.is_connected:
            await self.toggle_led(False)
            await self.__device_client.disconnect()

    @property
    def is_connected(self) -> bool:
        """Check if the TRIKI controller is connected"""
        return self.__device_client is not None and self.__device_client.is_connected

    @property
    def battery_level(self) -> int:
        """Get the TRIKI controller battery level"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read battery_level, because the TRIKI controller is not connected"
            )
        return self.__battery_level

    @property
    def firmware_version(self) -> str:
        """Get the TRIKI controller FW version"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read firmware_version, because the TRIKI controller is not connected"
            )
        return self.__firmware_version

    @property
    def spin_x(self) -> int:
        """Get the TRIKI controller X Spin value"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read spin_x, because the TRIKI controller is not connected"
            )
        return self.__sensor_spin_x

    @property
    def spin_y(self) -> int:
        """Get the TRIKI controller Y Spin value"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read spin_y, because the TRIKI controller is not connected"
            )
        return self.__sensor_spin_y

    @property
    def turn_z(self) -> int:
        """Get the TRIKI controller Z Turn value"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read turn_z, because the TRIKI controller is not connected"
            )
        return self.__sensor_turn_z

    @property
    def tilt_x(self) -> int:
        """Get the TRIKI controller X Tilt value"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read tilt_x, because the TRIKI controller is not connected"
            )
        return self.__sensor_tilt_x

    @property
    def tilt_y(self) -> int:
        """Get the TRIKI controller Y Tilt value"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read tilt_y, because the TRIKI controller is not connected"
            )
        return self.__sensor_tilt_y

    @property
    def flip_z(self) -> int:
        """Get the TRIKI controller Z Flip value"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read flip_z, because the TRIKI controller is not connected"
            )
        return self.__sensor_flip_z

    @property
    def button_pressed(self) -> bool:
        """Check if the TRIKI controller button is pressed"""
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot read button_pressed, because the TRIKI controller is not connected"
            )
        return self.__button_pressed

    async def toggle_led(self, is_on: bool) -> None:
        """
        Toggle the TRIKI controller built-in LED light

        Args:
            is_on:
                Set the LED status
        """
        if not self.is_connected:
            raise TRIKINotConnectedError(
                "Cannot toggle LED, because the TRIKI controller is not connected"
            )

        if is_on:
            bytes_to_send = bytes([0x01])
        else:
            bytes_to_send = bytes([0x00])

        await self.__device_client.write_gatt_char(
            LED_CHARACTERISTIC_UUID, bytes_to_send, response=True
        )

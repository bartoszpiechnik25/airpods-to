from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from binascii import hexlify
from time import time_ns
from typing import Any
from abc import ABC, abstractmethod, ABCMeta
import sys
import asyncio


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]


class SingletonABCMeta(SingletonMeta, ABCMeta):
    pass


class BluetoothDataReceiver(ABC, metaclass=SingletonABCMeta):
    @abstractmethod
    async def get_airpods_data(self) -> bytes:
        pass


class LinuxBluetoothDataReceiver(BluetoothDataReceiver):
    UPDATE_DURATION: int = 1
    MIN_RSSI: int = -60
    AIRPODS_MANUFACTURER: int = 76
    AIRPODS_DATA_LENGTH: int = 54
    RECENT_BEACONS_MAX_T_NS: int = 10000000000

    def __init__(self):
        self.__recent_beacons = []

    def __get_strongest_beacon(self, device: BLEDevice) -> BLEDevice:
        self.__recent_beacons.append({"time": time_ns(), "device": device})
        strongest_beacon = None
        i = 0
        while i < len(self.__recent_beacons):
            if time_ns() - self.__recent_beacons[i]["time"] > self.RECENT_BEACONS_MAX_T_NS:
                self.__recent_beacons.pop(i)
                continue
            if (
                strongest_beacon is None
                or strongest_beacon.rssi < self.__recent_beacons[i]["device"].rssi
            ):
                strongest_beacon = self.__recent_beacons[i]["device"]
            i += 1

        if strongest_beacon is not None and strongest_beacon.address == device.address:
            strongest_beacon = device

        return strongest_beacon

    async def get_airpods_data(self) -> bytes:
        devices = await BleakScanner.discover()
        for d in devices:
            d = self.__get_strongest_beacon(d)
            if (
                d.rssi >= self.MIN_RSSI
                and self.AIRPODS_MANUFACTURER in d.metadata["manufacturer_data"]
            ):
                data_hex = hexlify(
                    bytearray(d.metadata["manufacturer_data"][self.AIRPODS_MANUFACTURER])
                )
                data_length = len(
                    hexlify(bytearray(d.metadata["manufacturer_data"][self.AIRPODS_MANUFACTURER]))
                )
                if data_length == self.AIRPODS_DATA_LENGTH:
                    return data_hex
        return None


class WindowsBluetoothDataReceiver(BluetoothDataReceiver):
    async def get_airpods_data(self) -> bytes:
        await asyncio.sleep(0)  # This makes the method asynchronous
        return None


class MacOSBluetoothDataReceiver(BluetoothDataReceiver):
    def __init__(self) -> None:
        super().__init__()
        print("You have perfect support for AirPods on MacOS :)")
        sys.exit(0)

    async def get_airpods_data(self) -> bytes:
        await asyncio.sleep(0)  # This makes the method asynchronous
        return None


class BluetoothDataReceiverFactory:
    @staticmethod
    def get_bluetooth_data_receiver() -> BluetoothDataReceiver:
        mapping = {
            "linux": LinuxBluetoothDataReceiver,
            "win32": WindowsBluetoothDataReceiver,
            "darwin": MacOSBluetoothDataReceiver,
        }
        return mapping[sys.platform]()

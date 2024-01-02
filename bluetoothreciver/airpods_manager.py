from bluetoothreciver.parser import HexParser
from bluetoothreciver.bluetoothreciver import BluetoothDataReceiver
from asyncio import new_event_loop, set_event_loop, get_event_loop
from typing import Dict, Any, List
from observer.observer import Observer


class AirPodsManager:
    def __init__(self, observers: List[Observer] = None):
        self._bluetooth_reciver = BluetoothDataReceiver()
        self._observers: List[Observer] = observers or []

    def get_info(self) -> Dict[str, Any]:
        new_loop = new_event_loop()
        set_event_loop(new_loop)
        loop = get_event_loop()
        raw_data = loop.run_until_complete(self._bluetooth_reciver.get_airpods_data())
        loop.close()
        data = HexParser.parse(raw_data)
        self.notify(data)
        return data

    def notify(self, data: Dict[str, Any]) -> None:
        """
        Notify all observers about an event.

        Args:
            data (Dict[str, Any]): Data to send to observers.
        """
        for observer in self._observers:
            observer.update(data)

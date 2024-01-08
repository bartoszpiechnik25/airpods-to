from abc import ABC, abstractmethod
from typing import Dict, List
from state.state import HeadphonesBatteryState, LowBatteryState, MediumBatteryState


class Listener(ABC):
    @abstractmethod
    def update(self, data: Dict) -> None:
        pass


class GuiListener(Listener):
    def __init__(self, battery_state: LowBatteryState = LowBatteryState) -> None:
        super().__init__()
        self._battery_state: HeadphonesBatteryState = battery_state()

    def update(self, data: Dict) -> None:
        # Update the HeadphonesWindow with the new data
        self._battery_state.handle_gui(data)


class NotificationListener(Listener):
    def __init__(self, battery_state: LowBatteryState = MediumBatteryState) -> None:
        super().__init__()
        self._battery_state: HeadphonesBatteryState = battery_state()

    def update(self, data: Dict) -> None:
        # Update the HeadphonesWindow with the new data
        self._battery_state.handle_notification(data)


class TerminalListener(Listener):
    def __init__(self, battery_state: LowBatteryState = MediumBatteryState) -> None:
        super().__init__()
        self._battery_state: HeadphonesBatteryState = battery_state()

    def update(self, data: Dict) -> None:
        # Update the HeadphonesWindow with the new data
        self._battery_state.handle_notification(data)


class EventManager:
    def __init__(self, listeners: List[Listener] = None) -> None:
        self._listeners: Dict[str, Listener] = {}
        for listener in listeners:
            self._listeners[listener.__class__.__name__] = listener

    def subscribe(self, name: str, listener: Listener) -> None:
        if self._listeners is None:
            self._listeners = {}
        self._listeners[name] = listener

    def unsubscribe(self, name: str) -> None:
        if self._listeners is None:
            return
        self._listeners.pop(name)

    def notify(self, data) -> None:
        for listener in self._listeners:
            self._listeners[listener].update(data)

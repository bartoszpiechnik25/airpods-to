from abc import ABC, abstractmethod
from typing import Dict


class Observer(ABC):
    @abstractmethod
    def update(self, data: Dict) -> None:
        pass


class GuiObserver(Observer):
    def update(self, data: Dict) -> None:
        print(f"this is gui observer {data}")


class NotificationObserver(Observer):
    def update(self, data: Dict) -> None:
        print(f"this is notification observer {data}")


class DashMenuObserver(Observer):
    def update(self, data: Dict) -> None:
        print(f"this is dash menu observer {data}")

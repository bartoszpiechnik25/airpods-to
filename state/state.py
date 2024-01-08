from abc import ABC, abstractmethod

# from observer.observer import Listener
from pop_up_window.pop_up import HeadphonesWindow
from typing import Dict
from plyer import notification
import time

HISTORY = {"gui": [], "notification": []}


class HeadphonesBatteryState(ABC):
    @abstractmethod
    def handle_gui(self, data: Dict) -> None:
        pass

    @abstractmethod
    def handle_notification(self, data: Dict) -> None:
        pass

    @abstractmethod
    def handle_dash_menu(self, listener) -> None:
        pass


class LowBatteryState(HeadphonesBatteryState):
    # set update time to 5 mins
    UPDATE_TIME = 300
    GUI_PERCENTAGE = 20
    NOTIFICATION_PERCENTAGE = 50

    def handle_gui(self, data: Dict) -> None:
        if any(data["charge"][key] < self.GUI_PERCENTAGE for key in data["charge"]):
            update_time = time.time()

            if len(HISTORY["gui"]) == 0:
                HISTORY["gui"].append(update_time)
                percentage = data["charge"]
                self.headphones_window = HeadphonesWindow(
                    percentage["left"], percentage["right"], percentage["case"], data["model"]
                )

                # Show the HeadphonesWindow for 5 seconds
                self.headphones_window.show_and_destroy_after(5000)
            else:
                differece = update_time - HISTORY["gui"][0]
                if differece > self.UPDATE_TIME:
                    HISTORY["gui"][0] = update_time

                    percentage = data["charge"]
                    self.headphones_window = HeadphonesWindow(
                        percentage["left"], percentage["right"], percentage["case"], data["model"]
                    )

                    # Show the HeadphonesWindow for 5 seconds
                    self.headphones_window.show_and_destroy_after(5000)

    def handle_notification(self, data: Dict) -> None:
        if any(data["charge"][key] < self.NOTIFICATION_PERCENTAGE for key in data["charge"]):
            update_time = time.time()

            if len(HISTORY["notification"]) == 0:
                HISTORY["notification"].append(update_time)
                notification.notify(
                    title=f"{data['model']}",
                    message=f"Left: {data['charge']['left']}%\n"
                    + f"Right: {data['charge']['right']}%\n"
                    + f"Case: {data['charge']['case']}%",
                    app_icon="headphones-3-64.png",
                    timeout=4,
                    toast=False,
                )
            else:
                differece = update_time - HISTORY["notification"][0]
                if differece > self.UPDATE_TIME:
                    HISTORY["notification"][0] = update_time

                    notification.notify(
                        title=f"{data['model']}",
                        message=f"Left: {data['charge']['left']}%\n"
                        + f"Right: {data['charge']['right']}%\n"
                        + f"Case: {data['charge']['case']}%",
                        app_icon="headphones-3-64.png",
                        timeout=4,
                        toast=False,
                    )

    def handle_dash_menu(self, listener) -> None:
        pass

    def __str__(self) -> str:
        return (
            "LowBatteryState(\n"
            f"UPDATE_TIME: {self.UPDATE_TIME}\n"
            + f"GUI_PERCENTAGE: {self.GUI_PERCENTAGE}\n"
            + f"NOTIFICATION_PERCENTAGE: {self.NOTIFICATION_PERCENTAGE}\n)\n"
        )


class MediumBatteryState(HeadphonesBatteryState):
    UPDATE_TIME = 500
    GUI_PERCENTAGE = 50
    NOTIFICATION_PERCENTAGE = 70

    def handle_gui(self, data: Dict) -> None:
        if any(data["charge"][key] < self.GUI_PERCENTAGE for key in data["charge"]):
            update_time = time.time()

            if len(HISTORY["gui"]) == 0:
                HISTORY["gui"].append(update_time)
                percentage = data["charge"]
                self.headphones_window = HeadphonesWindow(
                    percentage["left"], percentage["right"], percentage["case"], data["model"]
                )

                # Show the HeadphonesWindow for 5 seconds
                self.headphones_window.show_and_destroy_after(5000)
            else:
                differece = update_time - HISTORY["gui"][0]
                if differece > self.UPDATE_TIME:
                    HISTORY["gui"][0] = update_time

                    percentage = data["charge"]
                    self.headphones_window = HeadphonesWindow(
                        percentage["left"], percentage["right"], percentage["case"], data["model"]
                    )

                    # Show the HeadphonesWindow for 5 seconds
                    self.headphones_window.show_and_destroy_after(5000)

    def handle_notification(self, data: Dict) -> None:
        if any(data["charge"][key] < self.NOTIFICATION_PERCENTAGE for key in data["charge"]):
            update_time = time.time()

            if len(HISTORY["notification"]) == 0:
                HISTORY["notification"].append(update_time)
                notification.notify(
                    title=f"{data['model']}",
                    message=f"Left: {data['charge']['left']}%\n"
                    + f"Right: {data['charge']['right']}%\n"
                    + f"Case: {data['charge']['case']}%",
                    app_icon="headphones-3-64.png",
                    timeout=4,
                    toast=False,
                )
            else:
                differece = update_time - HISTORY["notification"][0]
                if differece > self.UPDATE_TIME:
                    HISTORY["notification"][0] = update_time

                    notification.notify(
                        title=f"{data['model']}",
                        message=f"Left: {data['charge']['left']}%\n"
                        + f"Right: {data['charge']['right']}%\n"
                        + f"Case: {data['charge']['case']}%",
                        app_icon="headphones-3-64.png",
                        timeout=4,
                        toast=False,
                    )

    def handle_dash_menu(self, listener) -> None:
        pass

    def __str__(self) -> str:
        return (
            "MediumBatteryState(\n"
            f"UPDATE_TIME: {self.UPDATE_TIME}\n"
            + f"GUI_PERCENTAGE: {self.GUI_PERCENTAGE}\n"
            + f"NOTIFICATION_PERCENTAGE: {self.NOTIFICATION_PERCENTAGE}\n)\n"
        )


class HighBatteryState(HeadphonesBatteryState):
    GUI_UPDATE_TIME = 1800
    UPDATE_TIME = 500
    GUI_PERCENTAGE = 90
    NOTIFICATION_PERCENTAGE = 90

    def handle_gui(self, data: Dict) -> None:
        if any(data["charge"][key] < self.GUI_PERCENTAGE for key in data["charge"]):
            update_time = time.time()

            if len(HISTORY["gui"]) == 0:
                HISTORY["gui"].append(update_time)
                percentage = data["charge"]
                self.headphones_window = HeadphonesWindow(
                    percentage["left"], percentage["right"], percentage["case"], data["model"]
                )

                # Show the HeadphonesWindow for 5 seconds
                self.headphones_window.show_and_destroy_after(5000)
            else:
                differece = update_time - HISTORY["gui"][0]
                if differece > self.GUI_UPDATE_TIME:
                    HISTORY["gui"][0] = update_time

                    percentage = data["charge"]
                    self.headphones_window = HeadphonesWindow(
                        percentage["left"], percentage["right"], percentage["case"], data["model"]
                    )

                    # Show the HeadphonesWindow for 5 seconds
                    self.headphones_window.show_and_destroy_after(5000)

    def handle_notification(self, data: Dict) -> None:
        if any(data["charge"][key] < self.NOTIFICATION_PERCENTAGE for key in data["charge"]):
            update_time = time.time()

            if len(HISTORY["notification"]) == 0:
                HISTORY["notification"].append(update_time)
                notification.notify(
                    title=f"{data['model']}",
                    message=f"Left: {data['charge']['left']}%\n"
                    + f"Right: {data['charge']['right']}%\n"
                    + f"Case: {data['charge']['case']}%",
                    app_icon="headphones-3-64.png",
                    timeout=4,
                    toast=False,
                )
            else:
                differece = update_time - HISTORY["notification"][0]
                if differece > self.UPDATE_TIME:
                    HISTORY["notification"][0] = update_time

                    notification.notify(
                        title=f"{data['model']}",
                        message=f"Left: {data['charge']['left']}%\n"
                        + f"Right: {data['charge']['right']}%\n"
                        + f"Case: {data['charge']['case']}%",
                        app_icon="headphones-3-64.png",
                        timeout=4,
                        toast=False,
                    )

    def handle_dash_menu(self, listener) -> None:
        pass

    def __str__(self) -> str:
        return (
            "HighBatteryState(\n"
            f"GUI_UPDATE_TIME: {self.GUI_UPDATE_TIME}\n"
            + f"UPDATE_TIME: {self.UPDATE_TIME}\n"
            + f"GUI_PERCENTAGE: {self.GUI_PERCENTAGE}\n"
            + f"NOTIFICATION_PERCENTAGE: {self.NOTIFICATION_PERCENTAGE}\n)\n"
        )

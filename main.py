from bluetoothreciver.airpods_manager import AirPodsManager
from observer.observer import TerminalListener, NotificationListener, GuiListener
from state.state import MediumBatteryState, LowBatteryState, HighBatteryState
from time import sleep
import argparse

MAPPER = {"medium": MediumBatteryState, "low": LowBatteryState, "high": HighBatteryState}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Airpods battery notifier.")

    parser.add_argument("time", type=int, help="Time in seconds for starting the programme.")

    parser.add_argument(
        "gui_policy",
        type=str,
        default="low",
        choices=["low", "medium", "high"],
        help="".join(
            [
                "Available policies are: \n",
                "low - Notification more often from 20%%, \n",
                "medium - Notification starting from 50%%,\n",
                "high - Rare notification starting from 90%% with 30 min timeouts.\n",
            ]
        ),
    )

    parser.add_argument(
        "notification_policy",
        default="medium",
        type=str,
        choices=["low", "medium", "high"],
        help="".join(
            [
                "Available policies are: \n\n",
                "low - Notification more often from 20%%, \n",
                "medium - Notification starting from 50%%,\n",
                "high - Rare notification starting from 90%% with 30 min timeouts.\n",
            ]
        ),
    )
    args = parser.parse_args()

    dash_menu_Listener = TerminalListener()
    notification_Listener = NotificationListener(MAPPER[args.notification_policy])
    gui_Listener = GuiListener(MAPPER[args.gui_policy])

    manager = AirPodsManager([dash_menu_Listener, notification_Listener, gui_Listener])
    while True:
        data = manager.get_info()
        sleep(args.time)

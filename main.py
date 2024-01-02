from bluetoothreciver.airpods_manager import AirPodsManager
from observer.observer import DashMenuObserver, NotificationObserver, GuiObserver
from time import sleep
from plyer import notification

if __name__ == "__main__":
    # from tkinter import *

    # root = Tk()  # create a root widget
    # root.wm_attributes('-type', 'splash')
    # # root.title("Tk Example")
    # root.configure(background="yellow")
    # root.minsize(200, 200)  # width, height
    # root.maxsize(500, 500)
    # root.geometry("300x300+50+50")  # width x height + x + y
    # root.mainloop()
    dash_menu_observer = DashMenuObserver()
    notification_observer = NotificationObserver()
    gui_observer = GuiObserver()

    manager = AirPodsManager([dash_menu_observer, notification_observer, gui_observer])
    while True:
        data = manager.get_info()
        if data["status"] != 0:
            notification.notify(
                title=f"{data['model']}",
                message=f"Left: {data['charge']['left']}%\n"
                + f"Right: {data['charge']['right']}%\n"
                + f"Case: {data['charge']['case']}%",
                app_icon="headphones-3-64.png",
                timeout=4,
                toast=False,
            )
        sleep(15)

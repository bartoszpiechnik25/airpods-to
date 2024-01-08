import tkinter as tk
from PIL import Image, ImageTk
from abc import ABC, abstractmethod


class WindowComponentFactory:
    @staticmethod
    def create(component_type: str, window: tk.Toplevel, text: str):
        if component_type == "icon":
            return IconComponent(window, text)
        elif component_type == "label":
            return LabelComponent(window, text)
        else:
            raise ValueError("Invalid component type")


class WindowComponent(ABC):
    def __init__(self, window: tk.Toplevel, text: str):
        self.window = window
        self.text = text

    @abstractmethod
    def display(self):
        pass


class IconComponent(WindowComponent):
    def display(self):
        image = Image.open(self.text)  # Load the image with PIL
        self.image = ImageTk.PhotoImage(image)  # Convert the PIL image to a PhotoImage
        self.label = tk.Label(
            self.window, image=self.image, bg="grey"
        )  # Set the image option to the PhotoImage instance
        self.label.image = (
            self.image
        )  # Keep a reference to the image to prevent it from being garbage collected
        self.label.pack()


class LabelComponent(WindowComponent):
    def display(self):
        self.label = tk.Label(
            self.window, text=self.text, font=("Arial", 16), bg="grey", fg="white"
        )
        self.label.pack()


class HeadphonesWindow:
    def __init__(
        self, left_percentage: int, right_percentage: int, case_percentage: int, model: str
    ):
        self.root = tk.Tk()
        self.root.withdraw()

        self.window = tk.Toplevel()
        self.window.configure(bg="grey")
        self.window.geometry("150x150")
        self.window.title("Airpod status")

        self.left_label = WindowComponentFactory.create("label", self.window, f"{model}")

        self.icon = WindowComponentFactory.create(
            "icon", self.window, "/home/barti/airpods-to/headphones-3-64.png"
        )
        self.icon.display()

        self.left_label = WindowComponentFactory.create(
            "label", self.window, f"L: {left_percentage}%"
        )
        self.left_label.display()

        self.right_label = WindowComponentFactory.create(
            "label", self.window, f"R: {right_percentage}%"
        )
        self.right_label.display()

        self.case_label = WindowComponentFactory.create(
            "label", self.window, f"Case: {case_percentage}%"
        )
        self.case_label.display()

    def show_and_destroy_after(self, duration_ms):
        # Show the window
        self.root.update_idletasks()
        self.root.deiconify()

        # Schedule the destruction of the window after the specified duration
        self.root.after(duration_ms, self.destroy_window)
        self.root.withdraw()

        # Start the Tkinter event loop
        self.root.mainloop()

    def destroy_window(self):
        # Hide and destroy the window
        self.root.withdraw()
        self.root.destroy()

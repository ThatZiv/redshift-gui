from tkinter import *
import math
from enum import Enum
from src.redshift import Redshift
from src.db import DB

class Settings(Enum):
    TEMPERATURE="temp"
    BRIGHTNESS="brightness"

class RedshiftGUI:
    def __init__(self, master):
        self.rs = Redshift()
        self.db = DB("main.db")
        self.master = master
        master.title("Redshift GUI")
        master.minsize(300, 300)
        master.maxsize(300, 300)
        self.title = Label(master, text="Redshift GUI", font=("sans serif",25))
        self.close_button = Button(master, text="Close", background="red", foreground="white", command=master.quit)
        self.reset_button = Button(master, text="Reset", command=self.rs.reset)

        self.label_temperature = Label(master, text="Temperature")
        self.value_temperature = IntVar(value=self.db.get(Settings.TEMPERATURE.value) or 6500)
        # on scale change
        self.scale = Scale(master, from_=1000, to=10000, orient=HORIZONTAL, variable=self.value_temperature, length=200)
        self.change_button = Button(master,
                                          text="Change",
                                          background=self.convert_temperature_to_color_hex(),
                                          command=lambda: self.on_change_button())
        self.value_temperature.trace_add("write", lambda *args: self.change_button.config(background=self.convert_temperature_to_color_hex()))

        self.label_brightness = Label(master, text="Brightness")
        self.value_brightness = DoubleVar(value=self.db.get(Settings.BRIGHTNESS.value) or 1.0)
        self.brightness_scale = Scale(master, from_=0, to=1, resolution=0.05,
                                      variable=self.value_brightness,
                                      orient=HORIZONTAL, length=200)

        # layout packing
        self.title.pack()
        self.close_button.pack()
        self.reset_button.pack()
        self.label_brightness.pack()
        self.brightness_scale.pack()
        self.label_temperature.pack()
        self.scale.pack()
        self.change_button.pack()
        self.on_change_button() # init change based on stored values (or default values)

    def on_change_button(self):
        self.rs.change_color(self.value_temperature.get(), self.value_brightness.get())
        self.db.set(Settings.TEMPERATURE.value, self.value_temperature.get())
        self.db.set(Settings.BRIGHTNESS.value, self.value_brightness.get())

    def run(self):
        return self.master.mainloop()

    def convert_temperature_to_color_hex(self):
        temp = self.value_temperature.get()
        if temp < 1000 or temp > 10000:
            return "#ff0000"  # Red

        temp = temp / 100

        # Calculate red component
        if temp <= 66:
            red = 255
        else:
            red = temp - 60
            red = 329.698727446 * (red ** -0.1332047592)
            red = max(0, min(255, red))

        # Calculate green component
        if temp <= 66:
            green = temp
            green = 99.4708025861 * math.log(green) - 161.1195681661
            green = max(0, min(255, green))
        else:
            green = temp - 60
            green = 288.1221695283 * (green ** -0.0755148492)
            green = max(0, min(255, green))

        # Calculate blue component
        if temp >= 66:
            blue = 255
        else:
            if temp <= 19:
                blue = 0
            else:
                blue = temp - 10
                blue = 138.5177312231 * math.log(blue) - 305.0447927307
                blue = max(0, min(255, blue))

        return f"#{int(red):02x}{int(green):02x}{int(blue):02x}"

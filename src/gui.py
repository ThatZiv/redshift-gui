from tkinter import *
import math
from redshift import Redshift

class RedshiftGUI:
    def __init__(self, master):
        self.rs = Redshift()
        self.master = master
        master.title("Redshift GUI")
        master.minsize(300, 300)
        master.maxsize(300, 300)
        self.title = Label(master, text="Redshift GUI", font=("sans serif",25))
        self.title.pack()
        self.close_button = Button(master, text="Close", background="red", command=master.quit)
        self.close_button.pack()
        self.reset_button = Button(master, text="Reset", command=self.rs.reset)
        self.reset_button.pack()

        self.label_temperature = Label(master, text="Temperature")
        self.label_temperature.pack()
        self.value_temperature = DoubleVar()
        # on scale change
        self.scale = Scale(master, from_=1000, to=10000, orient=HORIZONTAL, variable=self.value_temperature, length=200)
        self.scale.pack()
        self.change_color_button = Button(master, text="Change Color", background=self.convert_temperature_to_color_hex(),command=lambda: self.rs.change_color(self.value_temperature.get()))
        self.change_color_button.pack()
        self.value_temperature.trace_add("write", lambda *args: self.change_color_button.config(background=self.convert_temperature_to_color_hex()))


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
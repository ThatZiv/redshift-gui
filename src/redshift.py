import subprocess
from time import sleep

# redshift -P -O 4200 -b 0.8

# Redshift API wrapper
class Redshift:
    def __init__(self) -> None:
        # check if redshift is installed
        try:
            subprocess.run(["redshift", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError as exc:
            raise FileNotFoundError("Redshift is not installed") from exc
        self.rs = None
    # Reset redshift color
    # @deprecated
    def reset(self):
        return subprocess.Popen(["redshift", "-x"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # change color based on temperature
    def change_color(self, temp: int, brightness: float = 1):
        if temp < 1000 or temp > 10000:
            raise ValueError("Temperature must be between 1000 and 10000")
        subprocess.run(["redshift", "-P", "-b", str(brightness), "-O", str(int(temp))], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

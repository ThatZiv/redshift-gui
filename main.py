from tkinter import Tk
import src.gui as gui

if __name__ == "__main__":
    # auto install tkinter if not installed
    try:
        import tkinter
    except ImportError:
        import pip
        pip.main(['install', 'tkinter'])
    root = Tk()
    gui = gui.RedshiftGUI(root)
    gui.run()

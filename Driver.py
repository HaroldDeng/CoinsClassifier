from tkinter import *
import random


"""
    |------------------------|
    |           |US conins   |
    |   video   |count; total|
    |           |------------|
    |-----------|xx conins   |
    |  setting  |count; total|
    |           |------------|
    |           |...         |
    |------------------------|
"""

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("480x480")
        self.root.title('A.I. Project')

        self.leftFrame = Frame(self.root)  # left side of the GUI
        self.leftFrame.pack(side=LEFT)
        self.rightFrame = Frame(self.root)  # right side of the GUI
        self.rightFrame.pack(side=RIGHT)



        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()

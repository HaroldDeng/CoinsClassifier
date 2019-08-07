from tkinter import *
import random

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("480x480")

        self.root.title('A.I. Project')

        msg = Label(self.root, text="If you see this, you are good",
                    font=("Arial", 16))

        def onClick():
            btn.configure(text = "You clicked")
        btn = Button(self.root, text="Click me", command=onClick)

        msg.grid(column = 0, row = 0)
        btn.grid(column = 0, row = 1)

        self.root.mainloop()

    def buttomClicked(self):
        print("Hello")



if __name__ == "__main__":
    gui = GUI()

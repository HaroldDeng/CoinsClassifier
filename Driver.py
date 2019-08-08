from tkinter import *


""" 2 windows
    -------------    --------------
    |           |    |US conins   |
    |   video   |    |count; total|
    |           |    |------------|
    |-----------|    |xx conins   |
    |  setting  |    |count; total|
    |           |    |------------|
    |           |    |...         |
    -------------    --------------
"""


class GUI:
    # WIDTH = 480
    # HEIGHT = 480

    def __init__(self):
        self.root = Tk()
        self.root.title("Image Window")

        self.imgFrame = Frame(self.root)
        self.imgFrame.grid(row=0, column=0)
        self.resFrame = Frame(self.root)
        self.resFrame.grid(row=0, column=1)

        self._inflateImg()
        self._inflateRes()
        self.imgFrame.mainloop()

    def _inflateImg(self):
        self.img = PhotoImage(file="img.ppm")
        self.canvas = Canvas(self.imgFrame)
        self.canvas.grid(row=0, column=0)
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)

        f = Frame(self.imgFrame)
        f.grid(row=1, column=0)
        Label(f, text="minRad", font="Helvetica, 15").grid(row=0, column=0)
        arg1 = Scale(f, from_=0, to=50, length=300, orient=HORIZONTAL)
        arg1.grid(row=0, column=1)

        Label(f, text="maxRad", font="Helvetica, 15").grid(row=1, column=0)
        arg2 = Scale(f, from_=0, to=50, length=300, orient=HORIZONTAL)
        arg2.grid(row=1, column=1)

    def _inflateRes(self):
        usCoinsValue = ["1¢", "5¢", "10¢", "25¢", "50¢", "$1"]
        self._inflateUS(usCoinsValue)

    def _inflateUS(self, value: [str]):
        x, y = 0, 0
        for val in value:
            # value
            Label(self.resFrame, text=val, font="Helvetica 16").grid(
                row=y, column=x)
            x += 1
            # count
            Label(self.resFrame, text=str(x)+str(y), font="Helvetica 20 bold", padx=20, anchor=W).grid(
                row=y, column=x)

            if x == 3:
                x = 0
                y += 1
            else:
                x += 1

        # Label(self.rightFrame, text="Total",
        #       font="Helvetica 30 bold").grid(row=2, column=0)
        # Label(self.rightFrame, text="$000",
        #       font="Helvetica 30 bold").grid(row=2, column=1)


if __name__ == "__main__":
    gui = GUI()

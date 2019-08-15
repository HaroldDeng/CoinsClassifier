#!/usr/bin/python3

from tkinter import *
import time, threading


""" 1 window
    -------------    --------------
    |           |    |US conins   |
    |   video   |    |.; total|
    |           |    |------------|
    |-----------|    |xx conins   |
    |  setting  |    |.; total|
    |           |    |------------|
    |           |    |...         |
    -------------    --------------
"""


class GUI:
    # WIDTH = 480
    # HEIGHT = 480
    usCoinsValue = ["1¢", "5¢", "10¢", "25¢", "50¢", "$1"]

    def __init__(self):
        self.input = [0, 0, 0, 0]
        self.labelList = []

        self.root = Tk()
        self.root.title("Image Window")

        self.imgFrame = Frame(self.root)
        self.imgFrame.grid(row=0, column=0)
        self.resFrame = Frame(self.root)
        self.resFrame.grid(row=0, column=1)

        self._inflateImg()
        self._inflateRes()
        threading.Thread(target=self._infiniteUpdate, args=()).start()
        self.imgFrame.mainloop()

    def _inflateImg(self):

        def listener(_):
            self.input[0] = acc.get()
            self.input[1] = minRad.get()
            self.input[2] = minDis.get()
            self.input[3] = dp.get()
            print(self.input)
            # pass

        self.img = PhotoImage(file="img.ppm")
        self.canvas = Canvas(self.imgFrame)
        self.canvas.grid(row=0, column=0)
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)

        f = Frame(self.imgFrame)
        f.grid(row=1, column=0)

        Label(f, text="accThr", font="Helvetica, 15").grid(row=0, column=0)
        acc = Scale(f, from_=0, to=100, length=300,
                    orient=HORIZONTAL, command=listener)
        acc.grid(row=0, column=1)

        Label(f, text="minRad", font="Helvetica, 15").grid(row=1, column=0)
        minRad = Scale(f, from_=0, to=100, length=300,
                       orient=HORIZONTAL, command=listener)
        minRad.grid(row=1, column=1)

        Label(f, text="minDis", font="Helvetica, 15").grid(row=2, column=0)
        minDis = Scale(f, from_=0, to=300, length=300,
                       orient=HORIZONTAL, command=listener)
        minDis.grid(row=2, column=1)

        Label(f, text="dp", font="Helvetica, 15").grid(row=3, column=0)
        dp = Scale(f, from_=0, to=5, length=300,
                   orient=HORIZONTAL, command=listener)
        dp.grid(row=3, column=1)

    def _inflateRes(self):
        self._inflateUS(self.usCoinsValue)

    def _inflateUS(self, value: [str]):
        x, y = 0, 0
        for val in value:
            # value
            Label(self.resFrame, text=val, font="Helvetica 16").grid(
                row=y, column=x)
            x += 1

            # labe
            lb = Label(self.resFrame, text=str(x)+str(y),
                       font="Helvetica 20 bold", padx=20, anchor=W)
            lb.grid(row=y, column=x)
            self.labelList.append(lb)

            if x == 3:
                x = 0
                y += 1
            else:
                x += 1

        y += 1
        x = 0
        Label(self.resFrame, text="Total",
              font="Helvetica 30 bold").grid(row=y, column=x, columnspan=2)
        x = 2
        lb = Label(self.resFrame, text="0.00", font="Helvetica 30 bold")
        lb.grid(row=y, column=x, columnspan=2)
        self.labelList.append(lb)

    def _infiniteUpdate(self):
        num = 1
        while True:
            for i in range(len(self.labelList)):
                if i < 6:
                    self.labelList[i].configure(text = str(num))
                else:
                    # ["1¢", "5¢", "10¢", "25¢", "50¢", "$1"]
                    total = num * (0.01 + 0.05 + 0.1 + 0.25 + 0.5 + 1)
                    self.labelList[i].configure(text = "{:10.2f}".format(total))
            num += 1
            time.sleep(0.5) # sleep for 0.2 second


if __name__ == "__main__":
    gui = GUI()

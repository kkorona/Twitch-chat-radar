#-*- coding: utf-8 -*-

import tkinter as tk
import graph_viewer
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import time

TOTAL_WIDTH = 1600
TOTAL_HEIGHT = 900

BOARDER_LINE = TOTAL_WIDTH / 10 * 4

LABEL_WIDTH = 25
TEXT_WIDTH = 12
LABEL_HEIGHT = 1

LABEL_VERTICAL_GAP = 20
LABEL_HORIZENTAL_GAP = 270
LABEL_LEFT_BOARDER = 40
LABEL_UPPER_BOARDER = 10

FRAME_HEIGHT = int(TOTAL_HEIGHT/10*3)
NAME_WIDTH = 5

tempNum = 1000
tempDate = "2019-01-15"
tempTime = "17:01:54"



class Frame:
    def __init__(self, parentFrame, grid_row, grid_col, _height, _width, frameName, name_enable):
        self.mainframe = tk.Frame(parentFrame, height = _height, width = _width, relief="solid", bd=1)
        self.mainframe.grid(column=grid_col, row=grid_row)
        if name_enable is True:
            self.addLabel(int(_height/10), NAME_WIDTH, frameName, 1)
            nameLabel = tk.Label(self.mainframe, relief="solid", height=_height, width=NAME_WIDTH, text=frameName, bd=1)
            nameLabel.pack(side=tk.LEFT)
        self.frameList = []
        self.textDict = {}

    
    def addLabel(self, _height, _width, _text, _bd):
        label = tk.Label(self.mainframe, relief = "solid", height=_height, width=_width, text=_text, bd=_bd)
        label.pack(side=tk.LEFT)

    def addText(self, _height, _width, textname, textVar):
        text = tk.Text(self.mainframe, height=_height, width=_width)
        updateText(text, textVar)
        self.textDict[textname] = text

    def addFrame(self, pos_x, pos_y, _height, _width, frameName):
        frame = Frame(self.mainframe, pos_x, pos_y, _height, _width, frameName, False)
        self.frameList.append(frame)


def updateText(text, textVariable):
    text.delete("1.0","end")
    text.insert(tk.END,textVariable)

def statInit(window):

    statFrame = Frame(window,0,0,FRAME_HEIGHT,BOARDER_LINE,"Log Stats", True)

    '''
    # frame name
    name = tk.Label(statFrame, height=FRAME_HEIGHT, width=NAME_WIDTH, text="Log Stats", bd=1)
    name.place(x=0, y=0)

    # number of chat
    curFrame = tk.Frame(statFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER, y=LABEL_UPPER_BOARDER)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="Number of Chat : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, str(tempNum))
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)
    
    # number of users
    curFrame = tk.Frame(statFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER, y=LABEL_UPPER_BOARDER + LABEL_VERTICAL_GAP)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="Number of Users : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, str(tempNum))
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)

    # start date
    curFrame = tk.Frame(statFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER, y=LABEL_UPPER_BOARDER + 2*LABEL_VERTICAL_GAP)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="Start Date : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, tempDate)
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)
     
    # start time
    curFrame = tk.Frame(statFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER, y=LABEL_UPPER_BOARDER + 3*LABEL_VERTICAL_GAP)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="Start Time : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, tempTime)
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)
    

    # end date
    curFrame = tk.Frame(statFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER, y=LABEL_UPPER_BOARDER + 4*LABEL_VERTICAL_GAP)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="End Date : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, tempDate)
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)

    # end time
    curFrame = tk.Frame(statFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER, y=LABEL_UPPER_BOARDER + 5*LABEL_VERTICAL_GAP)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="End Time : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, tempTime)
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)


    # current date
    curFrame = tk.Frame(statFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER + LABEL_HORIZENTAL_GAP, y=LABEL_UPPER_BOARDER)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="Current Date : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, tempDate)
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)

    # current time
    curFrame = tk.Frame(statFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER + LABEL_HORIZENTAL_GAP, y=LABEL_UPPER_BOARDER + LABEL_VERTICAL_GAP)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="Current Time : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, tempTime)
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)
    '''


def processingInit(window):
    processingFrame=tk.Frame(window,width = BOARDER_LINE, height = FRAME_HEIGHT, relief="solid",bd=1)
    processingFrame.place(x=0, y=TOTAL_HEIGHT/10*3)

    # number of chat
    curFrame = tk.Frame(processingFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER, y=LABEL_UPPER_BOARDER)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="Number of Chat : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, str(tempNum))
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)

def viewInit(window):
    viewFrame=tk.Frame(window,width = BOARDER_LINE, height = FRAME_HEIGHT, relief="solid",bd=1)
    viewFrame.place(x=0, y=TOTAL_HEIGHT/10*6)

    # number of chat
    curFrame = tk.Frame(viewFrame, height=LABEL_HEIGHT)
    curFrame.place(x=LABEL_LEFT_BOARDER, y=LABEL_UPPER_BOARDER)
    label = tk.Label(curFrame, relief="groove", height = LABEL_HEIGHT, width=LABEL_WIDTH, text="Number of Chat : ", bd=0)
    label.pack(side=tk.LEFT)
    # value
    text = tk.Text(curFrame, height = LABEL_HEIGHT, width = TEXT_WIDTH)
    text.insert(tk.CURRENT, str(tempNum))
    text.config(state="disabled")
    text.pack(side=tk.RIGHT)


def actionInit(window):
    actionFrame = tk.Frame(window, width=BOARDER_LINE, height = TOTAL_HEIGHT/10, relief="solid", bd=1)
    actionFrame.place(x=0, y=TOTAL_HEIGHT/10*9)


def radarInit(window):
    radarFrame=tk.Frame(window,width=TOTAL_WIDTH - BOARDER_LINE, height = TOTAL_HEIGHT / 10 * 7, relief="solid",bd=1)
    radarFrame.place(x=BOARDER_LINE, y=0)
    
    canvas = FigureCanvasTkAgg(graph_viewer.export_plt(), master=radarFrame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def consoleInit(window):
    consoleFrame=tk.Frame(window,width=TOTAL_WIDTH - BOARDER_LINE, height = TOTAL_HEIGHT / 10 * 3, relief="solid",bd=1)
    consoleFrame.place(x=BOARDER_LINE, y=TOTAL_HEIGHT / 10 * 7)


def main():
    window = tk.Tk()
    window.title("Twitch Char Radar")
    window.geometry(str(TOTAL_WIDTH)+"x"+str(TOTAL_HEIGHT)+"+50+50")
    window.resizable(False,False)

    statInit(window)
    '''
    processingInit(window)
    viewInit(window)
    actionInit(window)
    radarInit(window)
    consoleInit(window)
    '''
    
    window.mainloop()
    

if __name__ == "__main__":
    main()
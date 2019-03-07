#-*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import graph_viewer
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import ChattyParser
import datetime
import parser
import inspect
import HangeulParse

# Config Variables

LOG_PATH = "D:\\Twitch-chat-radar\\data\\logs\\"
STREAMER_TABLE = ("zilioner",)

TOTAL_WIDTH = 1600
TOTAL_HEIGHT = 900

BOARDER_LINE = TOTAL_WIDTH / 10 * 4

LABEL_WIDTH = 25
TEXT_WIDTH = 12
LABEL_HEIGHT = 1

textindex = None

LABEL_VERTICAL_GAP = 20
LABEL_HORIZENTAL_GAP = 270
LABEL_LEFT_BOARDER = 40
LABEL_UPPER_BOARDER = 10

FRAME_HEIGHT = int(TOTAL_HEIGHT/10*3)
NAME_WIDTH = 5
count = 0

tempNum = 1000
tempDate = "2019-01-16"
tempStreamer = "zilioner"
tempTime = "17:01:54"
diff = 0

# Branch Variables
getOut = False
simRun = False

# Updating Objects
canvas = None
currentTimeEntry = None

# Frame Links

statFrame = None
processingFrame = None
actionFrame = None
viewFrame = None
radarFrame = None
consoleFrame = None

# Configuration Data

configDict = {}
configTarget = {}


# Actions


def exitProgram():
    global getOut
    getOut = True

def stopLoop():
    global simRun
    simRun = False

def onSimulation(x):
    global simRun
    simRun = True
    global diff
    diff = x

def updateConfig(target, content):
    if isinstance(target, tk.Text):
        updateText(target, content)
    elif isinstance(target, tk.Entry):
        updateEntry(target, content)


def updateText(text, content):
    text.config(state=tk.NORMAL)
    text.delete('1.0',tk.END)
    text.insert(tk.END,content)
    text.config(state=tk.DISABLED)
    

def updateEntry(entry, content):
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.insert(tk.END, content)
    entry.config(state='readonly')

def statInit(window):
    global statFrame
    statFrame = tk.Frame(window, relief="solid", bd=1)
    statFrame.grid(row=0,column=0, sticky=tk.N+tk.E+tk.W+tk.S)

    # number of chat
    label = tk.Label(statFrame, relief="groove", text="Number of Chat : ", bd=0)
    label.grid(row=0, column=0)
    # value
    entry = tk.Entry(statFrame, width = TEXT_WIDTH)
    entry.insert(tk.END, str(tempNum))
    entry.config(state="readonly")
    entry.grid(row=0, column=1)
    
    # number of users
    label = tk.Label(statFrame, relief="groove", text="Number of Users : ", bd=0)
    label.grid(row=1, column=0)
    # value
    entry = tk.Entry(statFrame, width = TEXT_WIDTH)
    entry.insert(tk.END, str(tempNum))
    entry.config(state="readonly")
    entry.grid(row=1, column=1)

    # start date
    label = tk.Label(statFrame, relief="groove", text="Start Date : ", bd=0)
    label.grid(row=2, column=0)
    # value
    entry = tk.Entry(statFrame, width = TEXT_WIDTH)
    entry.insert(tk.END, tempDate)
    entry.config(state="readonly")
    entry.grid(row=2, column=1)
     
    # start time
    label = tk.Label(statFrame, relief="groove", text="Start Time : ", bd=0)
    label.grid(row=3, column=0)
    # value
    entry = tk.Entry(statFrame, width = TEXT_WIDTH)
    entry.insert(tk.END, tempTime)
    entry.config(state="readonly")
    entry.grid(row=3, column=1)
    

    # end date
    label = tk.Label(statFrame, relief="groove", text="End Date : ", bd=0)
    label.grid(row=4, column=0)
    # value
    entry = tk.Entry(statFrame, width = TEXT_WIDTH)
    entry.insert(tk.END, tempDate)
    entry.config(state="readonly")
    entry.grid(row=4, column=1)

    # end time
    label = tk.Label(statFrame, relief="groove", text="End Time : ", bd=0)
    label.grid(row=5, column=0)
    # value
    entry = tk.Entry(statFrame, width = TEXT_WIDTH)
    entry.insert(tk.END, tempTime)
    entry.config(state="readonly")
    entry.grid(row=5, column=1)


    # current date
    label = tk.Label(statFrame, relief="groove", text="Current Date : ", bd=0)
    label.grid(row=6, column=0)
    # value
    entry = tk.Entry(statFrame, width = TEXT_WIDTH)
    entry.insert(tk.END, tempDate)
    entry.config(state="readonly")
    entry.grid(row=6, column=1)

    # current time
    label = tk.Label(statFrame, relief="groove", text="Current Time : ", bd=0)
    label.grid(row=7, column=0)
    # value
    entry = tk.Entry(statFrame, width = TEXT_WIDTH)
    entry.insert(tk.END, tempTime)
    entry.config(state="readonly")
    entry.grid(row=7, column=1)
    global currentTimeEntry
    currentTimeEntry = entry


def processingInit(window):
    global processingFrame
    processingFrame=tk.Frame(window, relief="solid",bd=1)
    processingFrame.grid(row=1, column=0, sticky=tk.N+tk.E+tk.W+tk.S)

    mode = tk.IntVar()
    showArrow = tk.IntVar()

    # Animation Mode
    animationFrame = tk.Frame(processingFrame, relief = "solid", bd=0.5)
    animationFrame.pack(side = tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=1)

    animationFrameEnable = tk.Radiobutton(animationFrame, text="Animation Mode", variable = mode, value=1)
    animationFrameEnable.pack(side=tk.TOP)

    #Threshold
    label = tk.Label(animationFrame, relief="groove", text="Threshold", bd=0)
    label.pack(side=tk.TOP)
    # value
    animationThresholdEntry = tk.Entry(animationFrame, width = TEXT_WIDTH)
    animationThresholdEntry.pack(side=tk.TOP)

    #history Mode
    historyFrame = tk.Frame(processingFrame, relief="solid", bd=0.5)
    historyFrame.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.BOTH, expand=1)

    historyFrameEnable = tk.Radiobutton(historyFrame, text="History Mode", variable = mode, value=2)
    historyFrameEnable.pack(side=tk.TOP)

    #Threshold
    label = tk.Label(historyFrame, relief="groove", text="Threshold", bd=0)
    label.pack(side=tk.TOP)
    # value
    historyThresholdEntry = tk.Entry(historyFrame)
    historyThresholdEntry.pack(side=tk.TOP)

    arrowEnable = tk.Radiobutton(historyFrame, text="Show Arrow", variable = showArrow, value=3)
    arrowEnable.pack(side=tk.TOP)

    #Arrow Invisibility
    label = tk.Label(historyFrame, relief="groove", text="Arrow invisibility : ", bd=0)
    label.pack(side=tk.TOP)
    # value
    arrowInvisibilityEntry = tk.Entry(historyFrame)
    arrowInvisibilityEntry.pack(side=tk.TOP)
    

def viewInit(window):
    global viewFrame
    viewFrame=tk.Frame(window, relief="solid",bd=1)
    viewFrame.grid(row=2, column=0, sticky=tk.N+tk.E+tk.W+tk.S)

    axisvalues = ["Perfection","Harass","Bans","IsDonation"]

    label = tk.Label(viewFrame,text="X axis")
    label.grid(row=0, column = 0)
    XaxisCombo = ttk.Combobox(viewFrame, values = axisvalues)
    XaxisCombo.set("None")
    XaxisCombo.grid(row=0, column=1)

    label = tk.Label(viewFrame,text="Y axis")
    label.grid(row=0, column = 2)
    YaxisCombo = ttk.Combobox(viewFrame, values = axisvalues)
    YaxisCombo.set("None")
    YaxisCombo.grid(row=0, column=3)

    label = tk.Label(viewFrame, text="Time Rate")
    label.grid(row=1, column=0)
    timeRateEntry = tk.Entry(viewFrame)
    timeRateEntry.grid(row=1, column=1)

    label = tk.Label(viewFrame, text="Start Date")
    label.grid(row=2, column=0)
    startDateEntry = tk.Entry(viewFrame)
    startDateEntry.grid(row=2, column=1)

    label = tk.Label(viewFrame, text="End Date")
    label.grid(row=2, column=2)
    endDateEntry = tk.Entry(viewFrame)
    endDateEntry.grid(row=2, column=3)


def actionInit(window):
    global actionFrame
    actionFrame = tk.Frame(window, relief="solid", bd=1)
    actionFrame.grid(row=3, column=0, sticky=tk.N+tk.E+tk.W+tk.S)
    
    actionButtonFrame = tk.Frame(actionFrame, relief="solid", bd=0)
    actionButtonFrame.pack(expand=True)

    
    MButton = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="STOP", command = stopLoop)
    MButton.grid(row=0,column=0)
    RButton = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="→", command = lambda:onSimulation(1))
    RButton.grid(row=0,column=1)
    R100Button = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="50→", command = lambda:onSimulation(50))
    R100Button.grid(row=0, column=2)
    exitButton = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="exit", command = exitProgram)
    exitButton.grid(row=1, column=0, columnspan=3)


def radarInit(window):
    global radarFrame
    radarFrame=tk.Frame(window, relief="solid",bd=1)
    radarFrame.grid(row=0, column=1, rowspan=2, columnspan=2, sticky=tk.N+tk.E+tk.W+tk.S)
    
    global canvas
    result = graph_viewer.export_init_plt((tempStreamer,),(tempDate,))
    canvas = FigureCanvasTkAgg(result[0], master=radarFrame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    currentTime = result[1]
    global currentTimeEntry
    updateConfig(currentTimeEntry,currentTime)



def consoleInit(window):
    global consoleFrame
    consoleFrame=tk.Frame(window, relief="solid",bd=1)
    consoleFrame.grid(row=2, column=1, rowspan=2, columnspan=2, sticky=tk.N+tk.E+tk.W+tk.S)


def updateCanvas():
    global canvas
    global radarFrame
    global diff
    currentTime = graph_viewer.update_plt(diff)
    canvas.draw()
    global currentTimeEntry
    updateConfig(currentTimeEntry,currentTime)

def main():

    window = tk.Tk()
    window.title("Twitch Char Radar")
    #window.geometry(str(TOTAL_WIDTH)+"x"+str(TOTAL_HEIGHT)+"+50+50")
    window.resizable(False,False )

    statInit(window)
    processingInit(window)
    viewInit(window)
    actionInit(window)
    radarInit(window)
    consoleInit(window)
    global getOut
    global simRun
    cnt = 0
    while not getOut:

        if simRun is True:
            cnt += 1
            if cnt >= 1000:
                updateCanvas()
                cnt%=1000
        window.update()

    

if __name__ == "__main__":
    main()
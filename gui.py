#-*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
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
fps = 10000

tempNum = 1000
tempDate = "2019-03-20"
tempStreamer = "pikra10"
tempTime = "17:01:54"
diff = 5

# Branch Variables
simRun = False
logAccept = False
unlocked = True

# Objects to be Updated
canvas = None
logScrollText = None
streamerName = None
logStartDate = None

# Frame Links

statFrame = None
processingFrame = None
actionFrame = None
viewFrame = None
radarFrame = None
consoleFrame = None
window = None

# Configuration Data

entryList = {}
openEntryList = ['Log Amount', 'Frame Speed', 'X axis scale', 'Y axis scale']


# Actions


def exitProgram():
    global window
    window.destroy()

def stopLoop():
    global logAccept
    if logAccept == False:
        updateConsole('Please submit chat log information.')
    else:
        global simRun
        simRun = False
        global unlocked
        unlocked = True
        openEntry()
        updateConsole('Radar Stop')

def onSimulation(x):
    global logAccept
    if logAccept == False:
        updateConsole('Please submit chat log information.')
    else:
        global simRun
        global diff
        global fps
        simRun = True
        diffStr = entryList['Log Amount'].get()
        fpsStr = entryList['Frame Speed'].get()
        speedShow = '1'
        if x != 1:
            speedShow = diffStr
        consoleLog = "Current speed :" + speedShow + " logs per update"
        updateConsole(consoleLog)
        consoleLog = "Current frame speed :" + fpsStr
        updateConsole(consoleLog)
        if x == 1:
            diff = 1
        else:
            diff = int(diffStr)
        fps = int(fpsStr)

def getLogInfo():
    global logAccept
    global entryList
    global streamerName
    global logStartDate
    logAccept = True
    streamerName = entryList['Streamer'].get()
    logStartDate = entryList['Log Start Date'].get()


def updateStatFrame():
    global entryList
    updateConfig(entryList['Number of Chat'], str(graph_viewer.NUMBER_OF_CHAT))
    updateConfig(entryList['Number of Users'], str(graph_viewer.NUMBER_OF_USERS))
    updateConfig(entryList['Start Date'], graph_viewer.START_DATE)
    updateConfig(entryList['Start Time'], graph_viewer.START_TIME)
    updateConfig(entryList['Current Date'], graph_viewer.START_DATE)
    updateConfig(entryList['Current Time'], graph_viewer.START_TIME)
    updateConfig(entryList['End Date'], graph_viewer.END_DATE)
    updateConfig(entryList['End Time'], graph_viewer.END_TIME)


def updateConsole(content):
    logScrollText.insert(tk.INSERT,content+'\n')

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
    '''
    entry.insert(tk.END, str(tempNum))
    entry.config(state="readonly")
    '''
    global statFrame
    global entryList
    statFrame = tk.Frame(window, relief="solid", bd=1)
    statFrame.grid(row=0,column=0, sticky=tk.N+tk.E+tk.W+tk.S)
    entryKey = None

    # name of streamer
    label = tk.Label(statFrame, relief="groove", text="Streamer : ", bd=0)
    label.grid(row=0, column=2)
    # value
    entryKey = 'Streamer'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=0, column=3)

    # log start date
    label = tk.Label(statFrame, relief="groove", text="Log Start Date : ", bd=0)
    label.grid(row=1, column=2)
    # value
    entryKey = 'Log Start Date'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].insert(tk.END, 'yyyy-mm-dd')
    entryList[entryKey].grid(row=1, column=3)
    

    # number of chat
    label = tk.Label(statFrame, relief="groove", text="Number of Chat : ", bd=0)
    label.grid(row=0, column=0)
    # value
    entryKey = 'Number of Chat'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=0, column=1)
    entryList[entryKey].config(state='readonly')
    
    # number of users
    label = tk.Label(statFrame, relief="groove", text="Number of Users : ", bd=0)
    label.grid(row=1, column=0)
    # value
    entryKey = 'Number of Users'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=1, column=1)
    entryList[entryKey].config(state='readonly')

    # start date
    label = tk.Label(statFrame, relief="groove", text="Start Date : ", bd=0)
    label.grid(row=2, column=0)
    # value
    entryKey = 'Start Date'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=2, column=1)
    entryList[entryKey].config(state='readonly')
     
    # start time
    label = tk.Label(statFrame, relief="groove", text="Start Time : ", bd=0)
    label.grid(row=3, column=0)
    # value
    entryKey = 'Start Time'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=3, column=1)
    entryList[entryKey].config(state='readonly')

    # end date
    label = tk.Label(statFrame, relief="groove", text="End Date : ", bd=0)
    label.grid(row=4, column=0)
    # value
    entryKey = 'End Date'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=4, column=1)
    entryList[entryKey].config(state='readonly')

    # end time
    label = tk.Label(statFrame, relief="groove", text="End Time : ", bd=0)
    label.grid(row=5, column=0)
    # value
    entryKey = 'End Time'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=5, column=1)
    entryList[entryKey].config(state='readonly')

    # current date
    label = tk.Label(statFrame, relief="groove", text="Current Date : ", bd=0)
    label.grid(row=6, column=0)
    # value
    entryKey = 'Current Date'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=6, column=1)
    entryList[entryKey].config(state='readonly')

    # current time
    label = tk.Label(statFrame, relief="groove", text="Current Time : ", bd=0)
    label.grid(row=7, column=0)
    # value
    entryKey = 'Current Time'
    entryList[entryKey] = tk.Entry(statFrame, width = TEXT_WIDTH)
    entryList[entryKey].grid(row=7, column=1)
    entryList[entryKey].config(state='readonly')


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
    global diff
    global entryList
    viewFrame=tk.Frame(window, relief="solid",bd=1)
    viewFrame.grid(row=2, column=0, sticky=tk.N+tk.E+tk.W+tk.S)

    axisvalues = ["k-mer score", "karma score"]

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

    label = tk.Label(viewFrame, text="Log Amount")
    label.grid(row=1, column=0)
    entryList['Log Amount'] = tk.Entry(viewFrame)
    entryList['Log Amount'].grid(row=1, column=1)
    entryList['Log Amount'].insert(tk.END, '5')

    label = tk.Label(viewFrame, text="Frame Speed")
    label.grid(row=1, column=2)
    entryList['Frame Speed'] = tk.Entry(viewFrame)
    entryList['Frame Speed'].grid(row=1, column=3)
    entryList['Frame Speed'].insert(tk.END, '10000')

    label = tk.Label(viewFrame, text="X axis scale")
    label.grid(row=2, column=0)
    entryList['X axis scale'] = tk.Entry(viewFrame)
    entryList['X axis scale'].grid(row=2, column=1)
    entryList['X axis scale'].insert(tk.END,"200")

    label = tk.Label(viewFrame, text="Y axis scale")
    label.grid(row=2, column=2)
    entryList['Y axis scale'] = tk.Entry(viewFrame)
    entryList['Y axis scale'].grid(row=2, column=3)
    entryList['Y axis scale'].insert(tk.END,"200")


def actionInit(window):
    global actionFrame
    actionFrame = tk.Frame(window, relief="solid", bd=1)
    actionFrame.grid(row=3, column=0, sticky=tk.N+tk.E+tk.W+tk.S)
    
    actionButtonFrame = tk.Frame(actionFrame, relief="solid", bd=0)
    actionButtonFrame.pack(expand=True)

    submitButton = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="Submit", command=getLogInfo)
    submitButton.grid(row = 0, column = 0, columnspan =3)
    MButton = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="STOP", command = stopLoop)
    MButton.grid(row=1,column=0)
    RButton = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="→", command = lambda:onSimulation(1))
    RButton.grid(row=1,column=1)
    R100Button = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="→→", command = lambda:onSimulation(2))
    R100Button.grid(row=1, column=2)
    exitButton = tk.Button(actionButtonFrame, overrelief=tk.RAISED, text="exit", command = exitProgram)
    exitButton.grid(row=2, column=0, columnspan=3)


def radarInit(window):
    global radarFrame
    radarFrame=tk.Frame(window, relief="solid",bd=1)
    radarFrame.grid(row=0, column=1, rowspan=2, columnspan=2, sticky=tk.N+tk.E+tk.W+tk.S)
    
    global canvas
    #result = graph_viewer.export_init_plt((tempStreamer,),(tempDate,))
    result = graph_viewer.export_init_plt((streamerName,),(logStartDate,))
    canvas = FigureCanvasTkAgg(result, master=radarFrame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def consoleInit(window):
    INITIAL_LOG = "Radar started"
    global consoleFrame
    consoleFrame=tk.Frame(window, relief="solid",bd=1)
    consoleFrame.grid(row=2, column=1, rowspan=2, columnspan=2, sticky=tk.N+tk.E+tk.W+tk.S)
    global logScrollText
    logScrollText = tkst.ScrolledText(master = consoleFrame, wrap = tk.WORD, width=20, height=10)
    logScrollText.pack(fill=tk.BOTH, expand=True)
    updateConsole(INITIAL_LOG)


def updateCanvas():
    global canvas
    global radarFrame
    global diff
    global entryList

    prevXLimit = graph_viewer.X_AXIS_LIMIT
    prevYLimit = graph_viewer.Y_AXIS_LIMIT
    graph_viewer.X_AXIS_LIMIT = int(entryList['X axis scale'].get())
    graph_viewer.Y_AXIS_LIMIT = int(entryList['Y axis scale'].get())

    if prevXLimit != graph_viewer.X_AXIS_LIMIT or prevYLimit != graph_viewer.Y_AXIS_LIMIT:
        updateConsole("Current X Range : ["+str(-graph_viewer.X_AXIS_LIMIT)+","+str(graph_viewer.X_AXIS_LIMIT)+"]")
        updateConsole("Current Y Range : ["+str(-graph_viewer.Y_AXIS_LIMIT)+","+str(graph_viewer.Y_AXIS_LIMIT)+"]")

    updateResult = graph_viewer.update_plt(diff)
    logUpdate = updateResult
    canvas.draw()
    updateConfig(entryList['Current Date'], graph_viewer.currentDate)
    updateConfig(entryList['Current Time'],graph_viewer.currentTime)
    if logUpdate != "":
        updateConsole(logUpdate)

def lockEntry():
    for entryKey in entryList:
        entryList[entryKey].config(state='readonly')

def openEntry():
    global entryList
    global openEntryList
    for entryKey in openEntryList:
        entryList[entryKey].config(state='normal')

def main():
    global window
    window = tk.Tk()
    window.title("Twitch Char Radar")
    #window.geometry(str(TOTAL_WIDTH)+"x"+str(TOTAL_HEIGHT)+"+50+50")
    window.resizable(False,False)

    statInit(window)
    processingInit(window)
    viewInit(window)
    actionInit(window)
    consoleInit(window)
    global simRun

    # Section for getting log info
    window.update()

    while logAccept is False:
        window.update()

    radarInit(window)
    # 
    updateConsole("Current Log: "+graph_viewer.LOG_NAME)
    cnt = 0
    updateStatFrame()
    window.update()
    
    global unlocked

    while True:
        if simRun is True:
            if unlocked:
                lockEntry()
                unlocked = False
            cnt += 1
            if cnt >= fps:
                updateCanvas()
                cnt%=fps
        window.update()
    

if __name__ == "__main__":
    main()
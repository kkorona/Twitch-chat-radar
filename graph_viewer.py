import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from collections import namedtuple
import numpy as np
import ChattyParser
import HangeulParse
import random
import math

CONTENT_PATH = "D:\\Twitch-chat-radar\\data\\log_contents\\"
LOG_PATH = "D:\\Twitch-chat-radar\\data\\logs\\"
SCORE_WARNING_LIMIT = 0
BAN_WARNING_LIMIT = 0
AXIS_LIMIT = 200

Point = namedtuple("Point",("kmerScore","lengthScore"))
matplotlib.use("TkAgg")
myplot = None
fig = None
Color = namedtuple("Color",("recent", "abnormal"))
mycolor = Color('#8DD3C7', '#FF4444')

plt.style.use('dark_background')

chatData = None

points = None
startRef = 0
lastLogIndex = 0
userNote = {}
log = None

def init_points(streamer, date):
    result = ChattyParser.readFile(LOG_PATH, streamer, date)
    points = {}
    log_name = date[0] + "_#" + streamer[0] + ".log"
    print(log_name)
    global log
    global lastLogIndex
    log = result.get(log_name)
    _n = len(log)
    for i in range(1,101):
        if log[i] is None:
            continue
        if log[i]['type'] is not 'CHAT':
            continue
        lastLogIndex = i
        val = HangeulParse.getScore(log[i]['content'])
        kmerVal = val[0]
        lengthVal = math.log(val[1])
        idVal = log[i]['uname']
        if idVal in points:
            oldPoint = points.get(idVal)
            kmerVal = (kmerVal * 0.1 + oldPoint.kmerScore * 0.9)
            lengthVal = (lengthVal * 0.1 + oldPoint.lengthScore * 0.9)
        newPoint = Point(kmerScore=kmerVal, lengthScore=lengthVal)
        points[idVal] = newPoint
    return points


def create_plt(target_plot, points):
    recent_row = []
    recent_col = []
    old_row = []
    old_col = []
    warn_row = []
    warn_col = []
    for userID in points:
        point = points.get(userID)
        x = point.kmerScore
        y = point.lengthScore
        if x >= SCORE_WARNING_LIMIT and y >= BAN_WARNING_LIMIT:
            recent_row.append(x)
            recent_col.append(y)
        else:
            warn_row.append(x)
            warn_col.append(y)
    
    target_plot.plot(recent_row,recent_col,'o',color=mycolor.recent, markersize = 2)
    target_plot.plot(old_row,old_col,'o',color=mycolor.old, markersize = 2)
    target_plot.plot(warn_row,warn_col,'o',color=mycolor.abnormal, markersize = 2)


def show_plt(target_plot):
    plt.show()


def viewSetting(target_plot):
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    target_plot.spines['left'].set_position('center')
    target_plot.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    target_plot.spines['right'].set_color('none')
    target_plot.spines['top'].set_color('none')


    # Changing color of axes
    target_plot.spines['left'].set_color('g')
    target_plot.spines['bottom'].set_color('g')

    target_plot.tick_params(axis='x', colors='w')
    target_plot.tick_params(axis='y', colors='w')

    # Show ticks in the left and lower axes only
    target_plot.xaxis.set_ticks_position('bottom')
    target_plot.yaxis.set_ticks_position('left')

    # Setting axe range
    target_plot.set_xlim(-AXIS_LIMIT,AXIS_LIMIT)
    target_plot.set_ylim(-AXIS_LIMIT,AXIS_LIMIT)

    # draw circle area
    theta = np.linspace(-np.pi*10,np.pi*10,200)
    scales=list(range(10,50,10))
    for scale in scales:
        target_plot.plot(np.sin(theta)*scale,np.cos(theta)*scale, color='g', linewidth=0.1)

def export_init_plt(streamer, date):
    global points
    points = init_points(streamer,date)
    global fig
    fig = Figure(figsize=(6.3,6.3), dpi=100)
    global myplot
    myplot = fig.add_subplot(111)

    viewSetting(myplot)

    global lastLogIndex
    recentTime = str(log[lastLogIndex]['hour']) + ':' + str(log[lastLogIndex]['minute']) + ':' + str(log[lastLogIndex]['second'])

    global startRef 
    startRef = 101
    create_plt(myplot, points)
    return (fig,recentTime)

def update_plt(diff):
    global points
    global startRef
    global lastLogIndex
    for i in range(startRef,startRef+diff):
        if log[i] is None:
            continue
        if log[i]['type'] is not 'CHAT':
            continue
        lastLogIndex = i
        val = HangeulParse.getScore(log[i]['content'])
        kmerVal = val[0]
        lengthVal = val[1]
        idVal = log[i]['uname']
        if idVal in points:
            oldPoint = points.get(idVal)
            kmerVal = (kmerVal + oldPoint.kmerScore * 0.9) 
            lengthVal = (lengthVal + oldPoint.lengthScore * 0.9)
        newPoint = Point(kmerScore=kmerVal, lengthScore=lengthVal)
        points[idVal] = newPoint

    recentTime = str(log[lastLogIndex]['hour']) + ':' + str(log[lastLogIndex]['minute']) + ':' + str(log[lastLogIndex]['second'])

    startRef += diff
    global myplot
    myplot.clear()
    viewSetting(myplot)
    create_plt(myplot, points)
    return recentTime
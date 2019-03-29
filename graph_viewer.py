import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.scale as mscale
import matplotlib.transforms as mtransforms
import matplotlib.ticker as ticker
from collections import namedtuple
import numpy as np
import ChattyParser
import HangeulParse
import random
import math
import re

CONTENT_PATH = "D:\\Twitch-chat-radar\\data\\log_contents\\"
LOG_PATH = "D:\\Twitch-chat-radar\\data\\logs\\"
LOG_NAME = None
SCORE_WARNING_LIMIT = 0
BAN_WARNING_LIMIT = 0
X_AXIS_LIMIT = 200
Y_AXIS_LIMIT = 200
MIN_SHOW_FREQUENCY = 0
MAX_HOLD_FREQUENCY = 10
TIME_PERIOD_LIMIT = 600


Point = namedtuple("Point",("kmerScore","completionScore","time", "freq","id"))
matplotlib.use("TkAgg")
myplot = None
fig = None
Color = namedtuple("Color",("recent", "old", "abnormal", "bad", "subscriber"))
mycolor = Color('#5786D3', '#666699','#FF7F00', '#FF2222', '#BFFF00')

plt.style.use('dark_background')

chatData = None

points = None
startRef = 0
lastLogIndex = 0
userNote = {}
userList = set()
subsList = set()
banList = set()
permaBanList = set()
currentTime = None
currentDate = None
curTimeTick = 0
log = None

START_DATE = None
END_DATE = None
START_TIME = None
END_TIME = None
NUMBER_OF_CHAT = 0
NUMBER_OF_USERS = None

TIME_WEIGHT = {"year":32140800, "month":2678400, "day":86400, "hour":3600, "minute":60, "second":1}
TIME_KEY_LIST=["year","month","day","hour","minute","second"]

def convertTime(userInfo):
    result = 0
    for myKey in TIME_KEY_LIST:
        val = int(userInfo.get(myKey))
        if myKey is "year": 
            val -= 2010
        result += val * TIME_WEIGHT.get(myKey)
    return result

def init_points(streamer, date):
    result = ChattyParser.readFile(LOG_PATH, streamer, date)
    points = {}
    log_name = date[0] + "_#" + streamer[0] + ".log"
    global LOG_NAME
    global log
    global lastLogIndex
    global START_DATE
    global END_DATE 
    global START_TIME
    global END_TIME
    global NUMBER_OF_CHAT
    global startRef
    LOG_NAME = log_name
    log = result.get(log_name)
    _n = len(log)
    for i in range(1,_n):
        if log[i] is None:
            continue
        if log[i]['type'] != 'CHAT':
            continue
        if START_TIME is None:
            START_TIME = str(log[i]['hour']) + ':' + str(log[i]['minute']) + ':' + str(log[i]['second'])
            START_DATE = str(log[i]['year']) + '-' + str(log[i]['month']) + '-' + str(log[i]['day'])
            startRef=i
        END_TIME = str(log[i]['hour']) + ':' + str(log[i]['minute']) + ':' + str(log[i]['second'])
        END_DATE = str(log[i]['year']) + '-' + str(log[i]['month']) + '-' + str(log[i]['day'])
        NUMBER_OF_CHAT += 1
        userList.add(log[i]['uname'])

    global NUMBER_OF_USERS
    NUMBER_OF_USERS = len(userList)
    return points


def create_plt(target_plot, points):
    recent_row = []
    recent_col = []
    old_row = []
    old_col = []
    warn_row = []
    warn_col = []
    bad_row = []
    bad_col = []
    subs_row = []
    subs_col = []
    deleteList = []
    for userID in points:
        point = points.get(userID)
        x = point.kmerScore * 5
        y = point.completionScore * 5
        flag = True
        if point.freq < MIN_SHOW_FREQUENCY:
            flag = False
        '''
        elif (curTimeTick - point.time) >= TIME_PERIOD_LIMIT:
            deleteList.append(userID)
            flag = False
            continue    
        '''
        if flag is True:    
            if x > X_AXIS_LIMIT * 0.95:
                x = X_AXIS_LIMIT * 0.95
            if y > Y_AXIS_LIMIT * 0.95:
                y = Y_AXIS_LIMIT * 0.95
            if x < -X_AXIS_LIMIT * 0.95:
                x = -X_AXIS_LIMIT * 0.95
            if y < -Y_AXIS_LIMIT * 0.95:
                y = -Y_AXIS_LIMIT * 0.95
            
            #BAN APPLICATOIN
            if userID in permaBanList:
                bad_row.append(x)
                bad_col.append(y)
            elif userID in banList:
                warn_row.append(x)
                warn_col.append(y)
            elif userID in subsList:
                subs_row.append(x)
                subs_col.append(y)
            elif point.freq >= MAX_HOLD_FREQUENCY:
                old_row.append(x)
                old_col.append(y)
            else:
                recent_row.append(x)
                recent_col.append(y)
    
    target_plot.plot(recent_row,recent_col,'o',color=mycolor.recent, markersize = 2)
    target_plot.plot(old_row,old_col,'o',color=mycolor.old, markersize = 2)
    target_plot.plot(subs_row,subs_col,'o',color=mycolor.subscriber, markersize = 3)
    target_plot.plot(warn_row,warn_col,'o',color=mycolor.abnormal, markersize = 4)
    target_plot.plot(bad_row,bad_col,'o',color=mycolor.bad, markersize = 4)

    for userID in deleteList:
        del points[userID]


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

    # Setting squareroot scale
    # target_plot.xaxis.set_xscale('squareroot')
    # target_plot.yaxis.set_yscale('squareroot')

    # Setting axe range
    target_plot.set_xlim(-X_AXIS_LIMIT,X_AXIS_LIMIT)
    target_plot.set_ylim(-Y_AXIS_LIMIT,Y_AXIS_LIMIT)

    # draw circle area
    theta = np.linspace(-np.pi*10,np.pi*10,200)
    x_scales=list(range(0,X_AXIS_LIMIT+1,int(X_AXIS_LIMIT/4)))
    y_scales=list(range(0,Y_AXIS_LIMIT+1,int(Y_AXIS_LIMIT/4)))
    for (x_scale,y_scale) in zip(x_scales, y_scales):
        target_plot.plot(np.sin(theta)*x_scale,np.cos(theta)*y_scale, color='g', linewidth=0.1)

def brs(myFreq, curDistance):
    
    brsRet = (curDistance/10000) ** (1. / 2)
    if brsRet >= 0.99:
        return 0.99
    else:
        return brsRet
    
    

def export_init_plt(streamer, date):
    global points
    points = init_points(streamer,date)
    global fig
    fig = Figure(figsize=(6.3,6.3), dpi=100)
    global myplot
    myplot = fig.add_subplot(111)

    viewSetting(myplot)

    create_plt(myplot, points)
    return fig

def update_plt(diff):
    global points
    global startRef
    global lastLogIndex
    global curTimeTick
    consoleResult = ""
    for i in range(startRef,startRef+diff):
        if i >= len(log):
            continue
        if log[i] is None:
            continue
        if log[i]['type'] is 'CHAT':
            val = HangeulParse.getScore(log[i]['content'])
            kmerVal = val[0]
            completionVal = val[1]
            idVal = log[i]['uname']
            if log[i]['auth'].find('+') >= 0 :
                    subsList.add(idVal)
            timeVal = convertTime(log[i])
            curTimeTick = timeVal
            if not idVal in points:
                points[idVal] = Point(kmerScore=0, completionScore=0, time=timeVal, id=idVal, freq=0)
            oldPoint = points.get(idVal)
            freqVal = oldPoint.freq+1
            curDistance = oldPoint.kmerScore * oldPoint.kmerScore + oldPoint.completionScore * oldPoint.completionScore
            completionVal = completionVal*(1-brs(freqVal, curDistance)) + oldPoint.completionScore * brs(freqVal, curDistance)
            kmerVal = kmerVal*(1-brs(freqVal, curDistance)) + oldPoint.kmerScore * brs(freqVal, curDistance)
            newPoint = Point(kmerScore=kmerVal, completionScore=completionVal, id=idVal, time=timeVal, freq=freqVal)
            points[idVal] = newPoint
            
        elif log[i]['type'] is 'COMMAND':
            curType = log[i]['command']
            if curType == 'BAN':
                idVal = log[i]['target']
                consoleResult += "BAN:" + idVal
                timeVal = convertTime(log[i])
                curTimeTick = timeVal
                if not idVal in points:
                    points[idVal] = Point(kmerScore=0, completionScore=0, time=timeVal, id=idVal, freq=0)
                oldPoint = points.get(idVal)
                kmerVal = oldPoint.kmerScore
                if log[i]['attribute'] is None:
                    permaBanList.add(idVal)
                else:
                    banList.add(idVal)
                    consoleResult += "("+log[i]['attribute']+")"
                consoleResult+="\n"
                completionVal = oldPoint.completionScore       
                freqVal = oldPoint.freq + 1
                newPoint = Point(kmerScore=kmerVal, completionScore=completionVal, id = idVal, time=timeVal, freq=freqVal)
                points[idVal] = newPoint
                
        lastLogIndex = i
                

    global currentTime
    global currentDate
    lastLog = log[lastLogIndex]
    currentTime = str(lastLog['hour']) + ':' + str(lastLog['minute']) + ':' + str(lastLog['second'])
    currentDate = str(lastLog['year']) + '-' + str(lastLog['month']) + '-' + str(lastLog['day'])

    startRef += diff
    global myplot
    myplot.clear()
    viewSetting(myplot)
    create_plt(myplot, points)
    return consoleResult
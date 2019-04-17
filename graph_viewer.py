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
from collections import defaultdict
from collections import deque
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
X_AXIS_MAXIMUM = 200
X_AXIS_MINIMUM = -200
Y_AXIS_MAXIMUM = 200
Y_AXIS_MINIMUM = -200
MIN_SHOW_FREQUENCY = 0
MAX_HOLD_FREQUENCY = 10
TIME_PERIOD_LIMIT = 600
COOLING_RATE = 0.99
DEFINITE_TEMP = -200


Point = namedtuple("Point",("kmerScore","completionScore","time", "freq","id","noise"))
matplotlib.use("TkAgg")
myplot = None
fig = None
Color = namedtuple("Color",("recent", "old", "abnormal", "bad", "subscriber"))
mycolor = Color('#5786D3', '#666699','#FF7F00', '#FF2222', '#BFFF00')

plt.style.use('dark_background')

chatData = None

ax = None
annot = None
points = None
startRef = 0
lastLogIndex = 0
lastUserChat = {}
userList = set()
subsList = set()
banList = set()
permaBanList = set()
trackHistoryX = []
trackHistoryY = []
chatQueue = defaultdict(deque)
currentTime = None
currentDate = None
curTimeTick = 0
log = None

START_DATE = None
END_DATE = None
START_TIME = None
END_TIME = None
NUMBER_OF_CHAT = 0
NUMBER_OF_USERS = 0
EXP_FREQ_OF_CHAT = 0
TRACK_HISTORY_SIZE = 40

TEMP_BAN_VISIBILITY = False
SUBSCRIBER_VISIBILITY = False
NORMAL_VISIBILITY = False
REST_VISIBILITY = False
SHOW_TRACK_HISTORY = False
SHOW_TRACKER = False

TIME_WEIGHT = {"year":32140800, "month":2678400, "day":86400, "hour":3600, "minute":60, "second":1}
TIME_KEY_LIST=["year","month","day","hour","minute","second"]

def int2HexStr(x):
    if x > 255:
        return '00'
    p = int(x/16)
    q = x%16
    if p <= 5:
        p = chr(ord('F') - p)
    else:
        p = chr(ord('9') - p  + 6)

    if q <= 5:
        q = chr(ord('F') - q)
    else:
        q = chr(ord('9') - q + 6)
    return p+q

def convertTime(userInfo):
    result = 0
    for myKey in TIME_KEY_LIST:
        val = int(userInfo.get(myKey))
        if myKey is "year": 
            val -= 2010
        result += val * TIME_WEIGHT.get(myKey)
    return result

def squareConvert(target, LIMIT):
    calib = target / LIMIT
    if target < 0:
        calib = -calib
    calib = calib ** (3.0/4)
    calib *= LIMIT
    if target < 0:
        calib = -calib
    # print(str('%.2f' % target) + " -> " + str('%.2f' % calib))
    return calib

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
    global EXP_FREQ_OF_CHAT
    EXP_FREQ_OF_CHAT = float(NUMBER_OF_CHAT) / NUMBER_OF_USERS
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

    avgTemp = 0
    avgSimilarity = 0
    pointCnt = 0

    for userID in points:
        point = points.get(userID)
        x = point.kmerScore
        # x = squareConvert(x,X_AXIS_LIMIT)
        y = point.completionScore * COOLING_RATE ** (curTimeTick - point.time) + DEFINITE_TEMP
        # y = squareConvert(y,Y_AXIS_LIMIT)
        flag = True
        if REST_VISIBILITY is False and point.time + TIME_PERIOD_LIMIT < curTimeTick:                
                flag = False
    
        if flag is True:    
            if point.time + TIME_PERIOD_LIMIT > curTimeTick and y > 0:                
                avgTemp += y
                avgSimilarity += x
                pointCnt += 1

            if x > X_AXIS_MAXIMUM * 0.99:
                x = X_AXIS_MAXIMUM * 0.99
            if y > Y_AXIS_MAXIMUM * 0.99:
                y = Y_AXIS_MAXIMUM * 0.99
            if x < X_AXIS_MINIMUM * 0.99:
                x = X_AXIS_MINIMUM * 0.99
            if y < Y_AXIS_MINIMUM * 0.99:
                y = Y_AXIS_MINIMUM * 0.99

            #Show personal tracks
            if userID in permaBanList:
                bad_row.append(x)
                bad_col.append(y)
            elif userID in banList:
                if TEMP_BAN_VISIBILITY:
                    warn_row.append(x)
                    warn_col.append(y)
            elif userID in subsList:
                if SUBSCRIBER_VISIBILITY:
                    subs_row.append(x)
                    subs_col.append(y)
            elif point.time + TIME_PERIOD_LIMIT < curTimeTick:
                old_row.append(x)
                old_col.append(y)
            elif NORMAL_VISIBILITY:
                recent_row.append(x)
                recent_col.append(y)
    
    if SHOW_TRACK_HISTORY and len(trackHistoryX) >= TRACK_HISTORY_SIZE:
        st = len(trackHistoryX) - TRACK_HISTORY_SIZE
        ed = len(trackHistoryX)
        for i in range(st,ed):
            colorSize = int((ed-i)/TRACK_HISTORY_SIZE * 256)
            colorToken = '#' + int2HexStr(colorSize) * 3
            target_plot.plot(trackHistoryX[i-2:i], trackHistoryY[i-2:i],'-', color=colorToken)

    
    target_plot.plot(recent_row,recent_col,'o',color=mycolor.recent, markersize = 2)
    target_plot.plot(old_row,old_col,'o',color=mycolor.old, markersize = 2)
    target_plot.plot(subs_row,subs_col,'o',color=mycolor.subscriber, markersize = 3)
    target_plot.plot(warn_row,warn_col,'o',color=mycolor.abnormal, markersize = 4)
    target_plot.plot(bad_row,bad_col,'o',color=mycolor.bad, markersize = 4)

    if pointCnt > 0:
        avgTemp /= pointCnt
        avgSimilarity /= pointCnt
        trackHistoryX.append(avgSimilarity)
        trackHistoryY.append(avgTemp)
        if SHOW_TRACKER:
            target_plot.axhline(y=avgTemp, color='#777777', linestyle='-')
            target_plot.axvline(x=avgSimilarity, color='#777777', linestyle='-')
            target_plot.plot([avgSimilarity], [avgTemp], 'o', color='#777777', markersize = 6)



def show_plt(target_plot):
    plt.show()


def viewSetting(target_plot):
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    target_plot.spines['left'].set_position('zero')
    target_plot.spines['bottom'].set_position('zero')

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
    target_plot.set_xlim(X_AXIS_MINIMUM,X_AXIS_MAXIMUM)
    target_plot.set_ylim(Y_AXIS_MINIMUM,Y_AXIS_MAXIMUM)

    '''
    # draw circle area
    theta = np.linspace(-np.pi*10,np.pi*10,200)
    x_scales=list(range(0,X_AXIS_MAXIMUM+1,int(X_AXIS_MAXIMUM/4)))
    y_scales=list(range(0,Y_AXIS_MAXIMUM+1,int(Y_AXIS_MAXIMUM/4)))
    for (x_scale,y_scale) in zip(x_scales, y_scales):
        target_plot.plot(np.sin(theta)*x_scale,np.cos(theta)*y_scale, color='g', linewidth=0.1)
    '''


def brs(curTime, prevTime):
    
    if curTime <= prevTime:
        brsRet = 1
    else:
        brsRet = 1.0 / (curTime - prevTime) 
    return brsRet
    
    

def export_init_plt(streamer, date):
    global points
    points = init_points(streamer,date)
    global fig
    fig = Figure(figsize=(6.3,6.3), dpi=100)
    global myplot
    myplot = fig.add_subplot(111)
    global ax
    global annot
    ax = plt.subplot()
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))

    viewSetting(myplot)

    create_plt(myplot, points)
    return fig

def update_plt(diff):
    global points
    global startRef
    global lastLogIndex
    global curTimeTick
    global currentTime
    global currentDate
    consoleResult = []
    for i in range(startRef,startRef+diff):
        if i >= len(log):
            continue
        if log[i] is None:
            continue
        logContentVal = ""
        logTagVal = ""
        noiseVal = np.random.randn(1)[0] * Y_AXIS_MAXIMUM / 100 - Y_AXIS_MAXIMUM / 200
        if log[i]['type'] is 'CHAT':
            val = HangeulParse.getScore(log[i]['content'])
            kmerVal = val[0]
            completionVal = val[1] 
            idVal = log[i]['uname']
            cutIndex = idVal.find('(')
            if cutIndex != -1:
                idVal = idVal[cutIndex+1:-1]
            if log[i]['auth'].find('+') >= 0 :
                    subsList.add(idVal)
            timeVal = convertTime(log[i])
            chatQueue[idVal].append(timeVal)
            while chatQueue[idVal][0] + TIME_PERIOD_LIMIT < timeVal:
                chatQueue[idVal].popleft()
            result = ""
            for x in chatQueue[idVal]:
                result += str(x) + ' '
            # print(idVal + ': ' + result)
            lastUserChat[idVal] = log[i]['content']
            curTimeTick = timeVal
            if not idVal in points:
                points[idVal] = Point(kmerScore=kmerVal, completionScore=completionVal - DEFINITE_TEMP, id=idVal, time=timeVal, freq=1, noise = noiseVal)
            else:
                oldPoint = points.get(idVal)
                freqVal = oldPoint.freq+1
                kmerVal = kmerVal*(1-brs(curTimeTick, oldPoint.time)) + oldPoint.kmerScore * brs(curTimeTick, oldPoint.time)
                if oldPoint.completionScore > 0:
                    completionVal += oldPoint.completionScore
                newPoint = Point(kmerScore=kmerVal, completionScore=completionVal, id=idVal, time=timeVal, freq=freqVal, noise=noiseVal)
                points[idVal] = newPoint
            
        elif log[i]['type'] is 'COMMAND':
            curType = log[i]['command']
            if curType == 'BAN':
                idVal = log[i]['target']
                logContentVal = 'BAN:' + idVal
                timeVal = convertTime(log[i])
                curTimeTick = timeVal
                if not idVal in points:
                    points[idVal] = Point(kmerScore=0, completionScore=0, time=timeVal, id=idVal, freq=0, noise=noiseVal)
                oldPoint = points.get(idVal)
                kmerVal = oldPoint.kmerScore
                completionVal = oldPoint.completionScore 
                if log[i]['attribute'] is None:
                    permaBanList.add(idVal)
                    logContentVal = 'PERMA' + logContentVal
                    logTagVal = 'PERMABAN'
                else:
                    banList.add(idVal)
                    logContentVal += "("+log[i]['attribute']+")"
                    logTagVal = 'BAN'
                logContentVal += '(' + ('%.2f' % kmerVal) + ',' + ('%.2f' % completionVal) + ')'
                consoleResult.append((logContentVal,logTagVal))
                logTagVal = 'BANCONTENTS'
                logContentVal = "content: \"" + lastUserChat[idVal] + "\""
                consoleResult.append((logContentVal,logTagVal))   
                freqVal = oldPoint.freq + 1
                newPoint = Point(kmerScore=kmerVal, completionScore=completionVal, id = idVal, time=timeVal, freq=freqVal, noise=noiseVal)
                points[idVal] = newPoint
                
        lastLogIndex = i
                
    lastLog = log[lastLogIndex]
    currentTime = str(lastLog['hour']) + ':' + str(lastLog['minute']) + ':' + str(lastLog['second'])
    currentDate = str(lastLog['year']) + '-' + str(lastLog['month']) + '-' + str(lastLog['day'])

    startRef += diff
    global myplot
    myplot.clear()
    viewSetting(myplot)
    create_plt(myplot, points)
    return consoleResult
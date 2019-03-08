# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import ChattyParser
import HangeulParse as hp

LOG_PATH = "D:\\Twitch-chat-radar\\data\\logs\\"
STREAMER_TABLE = ("zilioner","dawnhs","flurry1989","lol_ambition","pacific8815","pikra10","pparkshy","rhdgurwns")
DATE = ("2019-01-15","2019-01-16","2019-01-17","2019-01-18","2019-01-21","2019-01-22","2019-01-23","2019-01-24","2019-01-28")
CONTENT_PATH = "D:\\Twitch-chat-radar\\data\\log_contents\\"

contentKeyList = ['complete','son','mom','alpha','special','number','etc']
contentinit = [0,0,0,0,0,0,0]
contentWeight = dict(zip(contentKeyList, [10,-2,-2,1,1,1,-1]))

MYMAX = 2000
SHOWLEN = 200

def buildContentDictList(size):
    ret = []
    for i in range(0,size):
        ret.append(dict(zip(contentKeyList,contentinit)))
    return ret

def main():
    chatData = ChattyParser.readFile(LOG_PATH, STREAMER_TABLE,DATE)
    print('collection finished')
    chatLimit = 0
    pltCnt = 1
    res = ""
    chatPrint = ""
    scoreData = []

    chart_numPerChat = plt.figure(1)
    chart_charPerChat = plt.figure(2)
    charPerChatCnt = buildContentDictList(MYMAX)
    chart_charPerLen = plt.figure(3)
    charPerLenCnt = buildContentDictList(MYMAX)
    chart_score = plt.figure(4)    

    for i in charPerChatCnt:
        for contentKey in contentKeyList:
            i[contentKey] = 0
    
    for i in charPerLenCnt:
        for contentKey in contentKeyList:
            i[contentKey] = 0
    

    for logName in chatData.keys():
        resVal = chatData.get(logName)
        attr = {'log name' : None, 'Topic':set(), '# of Chat' : 0, '# of Users' : 0, 'Average Chat per User' : 0, 'Average Chat Size per User' : 0 }
        userChatCount = {}
        userChatLenCount = {}
        userChatData = {}
        
        attr['log name'] = logName
        curLen = len(resVal)        
        if curLen <= 40000:
            continue
        for i in range(1, curLen):
            if resVal[i] is not None:
                if resVal[i]['type'] is 'CHAT':
                    attr['# of Chat'] += 1
                    chatPrint += resVal[i]['content'] + '\n'
                    userName = resVal[i]['uname']
                    userChatLen = len(resVal[i]['content'])
                    if userName in userChatCount:
                        userChatCount[userName] += 1
                    else:
                        userChatCount[userName] = 1

                    if userName in userChatLenCount:
                        userChatLenCount[userName] += userChatLen
                    else:
                        userChatLenCount[userName] = userChatLen

                    if chatLimit < userChatCount[resVal[i]['uname']]:
                        chatLimit = userChatCount[resVal[i]['uname']]

                    disformed = hp.disform(resVal[i]['content'])
                    scoreData.append(hp.getScore(resVal[i]['content'])[0])
                    if not userName in userChatData:
                        userChatData[userName] = {}
                        for contentKey in contentKeyList:
                            userChatData[userName][contentKey] = 0
                    curLen = len(resVal[i]['content'])
                    for contentKey in contentKeyList:
                        userChatData[userName][contentKey] += len(disformed.get(contentKey))
                        charPerLenCnt[curLen][contentKey] += len(disformed.get(contentKey))
                    
                    
                if resVal[i]['type'] is 'TITLE':
                    attr['Topic'].add(resVal[i]['category'])

        attr['# of Users'] = len(userChatCount)
        '''
        for i in range(0,10):
            print(charPerChatCnt[i]['complete'])
        print('-------------------------')
        '''

        chatCount = [0,] * (chatLimit+1)
        for userName in userChatCount:
            chatCount[userChatCount.get(userName)] += 1
            attr['Average Chat per User'] += userChatCount.get(userName)
            for contentKey in contentKeyList:
                charPerChatCnt[userChatCount.get(userName)][contentKey] += userChatData[userName][contentKey]
            print(str(charPerChatCnt[0]['complete']) + ' ' + str(charPerChatCnt[1]['complete']))
        
        for userName in userChatLenCount:
            attr['Average Chat Size per User'] += userChatLenCount[userName] / userChatCount.get(userName)
        attr['Average Chat per User'] /= attr['# of Users']
        attr['Average Chat Size per User'] /= attr['# of Users']
        # # of Chat / Chat per User Graph
        
        curPlot = chart_numPerChat.add_subplot(2,5,pltCnt)
        pltCnt += 1

        curPlot.set_yscale('log')
        xval = range(1,50)
        curPlot.plot(xval,chatCount[1:50],'ro')

        curPlot.set_xlabel('Chat per Users\n('+logName+')')
        curPlot.set_ylabel('# of User')

        for key in attr:
            val = attr.get(key)
            res += key + ': ' + str(val) + '\n'
        res += '----------------------\n\n'

        # Chat Clipping
        with open(CONTENT_PATH + logName,'w', encoding="UTF8") as ff:
            ff.write(chatPrint)
        

    xval = range(0,SHOWLEN)
    # char per chat
    pltCnt = 1
    keylen = len(contentKeyList)
    for contentKey in contentKeyList:
        curPlot = chart_charPerChat.add_subplot(keylen,1,pltCnt)
        yval = [0,]*SHOWLEN
        for i in xval:
            yval[i] = charPerChatCnt[i][contentKey]
        curPlot.set_xlabel('# of Chat')
        curPlot.set_ylabel(contentKey)
        curPlot.plot(xval,yval,'ro')
        pltCnt += 1

    # char per len
    pltCnt = 1
    keylen = len(contentKeyList)
    for contentKey in contentKeyList:
        curPlot = chart_charPerLen.add_subplot(keylen,1,pltCnt)
        yval = [0,]*SHOWLEN
        for i in xval:
            yval[i] = charPerLenCnt[i][contentKey]
        curPlot.set_xlabel('Chatting length')
        curPlot.set_ylabel(contentKey)
        curPlot.plot(xval,yval,'ro')
        pltCnt += 1


    # score histogram
    curPlot = chart_score.add_subplot(111)
    
    curPlot.hist(x=scoreData, bins=19, range=(-150,400), rwidth=0.8)
    plt.show()


    # Attribute Log
    '''
    with open('attrLog.txt','w') as f:
        f.write(res)
    '''
    

if __name__ == '__main__':
    main()

            
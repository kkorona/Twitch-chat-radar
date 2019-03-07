#-*- coding: utf-8 -*-

import re

CHAT_RE_FORMAT = r'\[(?P<date>(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))\] <(?P<auth>[\+\~\@\%\$\^\*\!\&]*)(?P<uname>(.)*)> (?P<content>(.)*)'
TITLE_RE_FORMAT = r'\[(?P<date>(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))\] ~(?P<title>(.)*)\((?P<category>(.)*)\)~'
COMMAND_RE_FORMAT = r'\[(?P<date>(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))\] (?P<command>\w+): (?P<target>\w+)(?P<attribute> \((\w+)\))?'

VARIOUS = ['CHAT', 'TITLE', 'COMMAND']
GROUPS={}
GROUPS['CHAT'] = ('date', 'year', 'month', 'day', 'hour', 'minute', 'second', 'auth', 'uname', 'content')
GROUPS['TITLE'] = ('date', 'year', 'month', 'day', 'hour', 'minute', 'second', 'title', 'category')
GROUPS['COMMAND'] = ('date', 'year', 'month', 'day', 'hour', 'minute', 'second', 'command', 'target', 'attribute')

chatp = re.compile(CHAT_RE_FORMAT)
titlep = re.compile(TITLE_RE_FORMAT)
commandp = re.compile(COMMAND_RE_FORMAT)
parseList = {'CHAT':chatp, 'TITLE':titlep, 'COMMAND':commandp}

def readFile(LOG_PATH, STREAMER_TABLE, DATE):

    ret = {}

    for date in DATE:
        for streamer in STREAMER_TABLE:
            streamer_path = LOG_PATH + "#" + streamer + "\\"
            log_name = date + "_#" + streamer + ".log"
            logs = []
            print(streamer_path + log_name)
            try:
                with open(streamer_path + log_name, "r", encoding='UTF8') as f:
                    logs = f.readlines()
            except FileNotFoundError:
                continue
            count = 0
            ret[log_name] = [None] * (len(logs) + 1)
            for log in logs:
                count = count + 1
                flag = False
                for logType in VARIOUS:
                    if flag:
                        break
                    curret = {}
                    p = parseList[logType]
                    m = p.search(log)
                    if m is not None :
                        curret['type'] = logType
                        for attr in GROUPS[logType]:
                            curret[attr] = m.group(attr)
                        ret[log_name][count]=curret
                        flag = True
                        break
                if flag is False:
                    ret[log_name][count]=None
    return ret




def main():
    LOG_PATH = "D:\\Twitch-chat-radar\\data\\logs\\"
    STREAMER_TABLE = ("zilioner",)
    DATE = ("2019-01-15","2019-01-16","2019-01-17","2019-01-18","2019-01-21","2019-01-22","2019-01-23","2019-01-24","2019-01-28")
    result = readFile(LOG_PATH, STREAMER_TABLE, DATE)
    for key in result.keys():
        resVal = result.get(key)
        if resVal is None:
            continue
        _n = len(resVal)
        for i in range(1,_n):
            if resVal[i] is not None:
                if resVal[i]['type'] is 'CHAT':
                    print(resVal[i]['content'] + '///' + str(len(resVal[i]['content'])))

if __name__ == "__main__":
    main()
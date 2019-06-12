#-*- coding: utf-8 -*-

import re

CHAT_RE_FORMAT = r'\[(?P<date>(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))\] <(?P<auth>[\+\~\@\%\$\^\*\!\&]*)(?P<uname>(.)*)> (?P<content>(.)*)'
TITLE_RE_FORMAT = r'\[(?P<date>(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))\] ~(?P<title>(.)*)\((?P<category>(.)*)\)~'
COMMAND_RE_FORMAT = r'\[(?P<date>(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))\] (?P<command>\w+): (?P<target>\w+)(?P<attribute> \((\w+)\))?'
INFO_RE_FORMAT = r'\[(?P<date>(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))\] \[Info\] This room is now in slow mode. You may send messages every (?P<slowrate>\d+) seconds.'
MELTSLOW_RE_FORMAT = r'\[(?P<date>(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))\] [Info] This room is no longer in slow mode.'

VARIOUS = ['CHAT', 'TITLE', 'COMMAND', 'INFO', 'MELTSLOW']
GROUPS={}
GROUPS['CHAT'] = ('date', 'year', 'month', 'day', 'hour', 'minute', 'second', 'auth', 'uname', 'content')
GROUPS['TITLE'] = ('date', 'year', 'month', 'day', 'hour', 'minute', 'second', 'title', 'category')
GROUPS['COMMAND'] = ('date', 'year', 'month', 'day', 'hour', 'minute', 'second', 'command', 'target', 'attribute')
GROUPS['INFO'] = ('date', 'year', 'month', 'day', 'hour', 'minute', 'second', 'slowrate')
GROUPS['MELTSLOW'] = ('date', 'year', 'month', 'day', 'hour', 'minute', 'second')

chatp = re.compile(CHAT_RE_FORMAT)
titlep = re.compile(TITLE_RE_FORMAT)
commandp = re.compile(COMMAND_RE_FORMAT)
infop = re.compile(INFO_RE_FORMAT)
meltslowp = re.compile(MELTSLOW_RE_FORMAT)
parseList = {'CHAT':chatp, 'TITLE':titlep, 'COMMAND':commandp, 'INFO':infop, 'MELTSLOW':meltslowp}

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
    STREAMER_TABLE = ("mbcmlt1",)
    DATE = ("2019-04-06",)
    result = readFile(LOG_PATH, STREAMER_TABLE, DATE)
    for key in result.keys():
        resVal = result.get(key)
        if resVal is None:
            continue
        _n = len(resVal)
        for i in range(1,30):
            mres = str(i)
            if resVal[i] is not None:
                mres += resVal[i]['type']
                if resVal[i]['type'] is 'INFO':
                    print(resVal[i]['slowrate'])
            print(mres)

if __name__ == "__main__":
    main()
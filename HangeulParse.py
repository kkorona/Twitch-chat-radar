import konlpy.tag as klp
import re
import math
import dictCheck

contentKeyList = ['complete','son','mom','alpha','special','number','etc']
contentWeight = dict(zip(contentKeyList, [17,-3,-3,2,2,0,-10]))

completeToken = r'[가-힣]'
sonToken = r'[ㄱ-ㅎ]'
momToken = r'[ㅏ-ㅣ]'
alphaToken = r'[a-zA-Z]'
specialToken = r'[\*\/\-\~\!\.\?\+\-\\\(\)]'
numberToken = r'\d'
etcToken = r'[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z\*\/\-\~\!\.\?\+\-\\\(\)\d\s]'

completeRE = re.compile(completeToken)
sonRE = re.compile(sonToken)
momRE = re.compile(momToken)
alphaRE = re.compile(alphaToken)
specialRE = re.compile(specialToken)
numberRE = re.compile(numberToken)
etcRE = re.compile(etcToken)

REs = [completeRE, sonRE, momRE, alphaRE, specialRE, numberRE, etcRE]
symbols = "kcvesnx"

def symbolize(targetString):
    ret = ''
    for x in targetString:
        if x is ' ':
            ret += ' '
            continue

        for i in range(0,len(REs)):
            if REs[i].match(x) is not None:
                ret += symbols[i]
                break
    return ret

def getScore(targetString):
    targetObj = disform(targetString)
    ret1 = 0.0
    ret2 = 100
    ret1 += targetObj['1mer'] + targetObj['2mer']
    ret2 += len(targetObj['son']) * contentWeight['son'] + len(targetObj['mom']) * contentWeight['mom'] + len(targetObj['etc']) * contentWeight['etc']
    return (ret1,ret2)
    

def disform(targetString):
    ret = {}

    complete = completeRE.findall(targetString)
    son = sonRE.findall(targetString)
    mom = momRE.findall(targetString)
    alpha = alphaRE.findall(targetString)
    special = specialRE.findall(targetString)
    number = numberRE.findall(targetString)
    etc = etcRE.findall(targetString)

    ret['complete'] = complete
    ret['son'] = son
    ret['mom'] = mom
    ret['alpha'] = alpha
    ret['special'] = special
    ret['number'] = number
    ret['etc'] = etc
    ret['1mer'] = 0
    for char in targetString:
        if char == ' ':
            continue
        ret['1mer'] += dictCheck.return_kmer(char)
    if ret['1mer'] > 0:
        ret['1mer'] = math.sqrt(ret['1mer'])
    else:
        ret['1mer'] = -math.sqrt(-ret['1mer'])
    ret['2mer'] = 0
    for mySplit in targetString.split():
        newTargetString = ' ' + mySplit + ' '
        for i in range(0,len(newTargetString)-1):
            content = newTargetString[i]+newTargetString[i+1]
            ret['2mer'] += dictCheck.return_kmer(content)
    return ret


if __name__ == '__main__':
    test = u'선Q쓰지 마시고 일단 E로 끄는 것 부터 생각하세요ㅋㅋㅋ. W는 。아끼는게 좋고 궁은 막 쓰세요.'
    val = disform(test)
    for key in val:
        print(key + ": " + str(val.get(key)))
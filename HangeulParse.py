import re
import math
import dictCheck
from myOperations import absoluteSquare
contentKeyList = ['complete','son','mom','alpha','special','number','etc']
contentKeyWeight = [4,-3,-3,0,0,0,-4]
contentWeight = dict(zip(contentKeyList, contentKeyWeight))

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

def count3gramComplete(tagretString):
    compCnt = 0
    etcCnt = 0
    if len(tagretString) >= 3:
        for i in range(0,len(tagretString) - 3):
            targetToken = tagretString[i:i+3]
            complete = completeRE.findall(targetToken)
            if len(complete) >= 1:
                compCnt += 1
            else:
                etcCnt += 1
    if(compCnt + etcCnt == 0):
        etcCnt = 1
    return float(compCnt) / (compCnt + etcCnt)

def countRunComplete(targetString):
    tokenCount = {}
    for character in targetString:
        '''
        # print(character + "/ " + str(runCount))
        if prev is None:
            prev = character
            continue
        if character == prev:
            continue
        '''
        tokenCount[character] = True
        '''
        runCount += 1
        if prev == ' ':
            runCount -= 1
        prev = character
        '''
    return len(tokenCount)


def getScore(targetString):
    # targetObj = disform(targetString)
    completionRet = 0
    # kmerRet = targetObj['1mer'] + targetObj['2mer'] + targetObj['3mer']
    completionRet = (countRunComplete(targetString)**1.5) * math.sqrt(float(len(targetString)))
    return (0,completionRet)
    

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
    merCount1 = 0
    for char in targetString:
        if char == ' ':
            continue
        ret['1mer'] += dictCheck.return_kmer(char)
        merCount1 += 1
    ret['1mer'] /= merCount1

    ret['2mer'] = 0
    ret['3mer'] = 0
    merCount2 = 0
    merCount3 = 0
    for mySplit in targetString.split():
        newTargetString = ' ' + mySplit + ' '
        for i in range(0,len(newTargetString)-1):
            content = newTargetString[i:i+2]
            merval = dictCheck.return_kmer(content)
            ret['2mer'] += merval
            merCount2 += 1
        for i in range(0,len(newTargetString)-2):
            content = newTargetString[i:i+3]
            merval = dictCheck.return_kmer(content)
            ret['3mer'] += merval
            merCount3 += 1
    ret['2mer'] /= merCount2
    ret['2mer'] = absoluteSquare(ret['2mer'],1.2)
    ret['3mer'] /= merCount3
    ret['3mer'] = absoluteSquare(ret['3mer'],1.5)
    return ret


if __name__ == '__main__':
    print(countRunComplete('비비비비비 비비비비비 비둘기 비둘기 비둘기기기기기'))
    print(countRunComplete('ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ'))
import json
import math
import matplotlib.pyplot as plt
from pprint import pprint

PATH_1MER = r'D:\Data\joongangdict\Joongang1merDicPy.json'
PATH_2MER = r'D:\Data\joongangdict\Joongang2merDicPy.json'
PATH_3MER = r'D:\Data\joongangdict\Joongang3merDicPy.json'

CUT_1MER = 23.15/2
CUT_2MER = 22.10/2
CUT_3MER = 20.36/2

f = lambda x : math.log(x,2)

with open(PATH_1MER,'r') as f_1mer:
    data_1mer = json.load(f_1mer)

with open(PATH_2MER,'r') as f_2mer:
    data_2mer = json.load(f_2mer)

with open(PATH_3MER, 'r') as f_3mer:
    data_3mer = json.load(f_3mer)


def show_kmer(s_mer):
    global f
    show = []

    for merkey in s_mer:
        val = f(s_mer.get(merkey))
        show.append(val)

    show.sort()
    xl = range(0,len(show))
    print(show[-1])

    plt.ylabel('Log(frequency)')
    plt.xlabel('Sorted k-mer value index')
    plt.title('k-mer histogram')
    plt.plot(xl,show)
    #plt.hist(show,bins=range(0,100,1), rwidth = 0.8)
    plt.show()

    with open("res.txt",'w', encoding='utf-16') as f:
        pprint(show,f)

def return_kmer(targetToken):
    global f
    result = 0
    if len(targetToken) is 1:
        if targetToken in data_1mer:
            result = f(data_1mer[targetToken])
        result -= CUT_1MER
    elif len(targetToken) is 2:
        cnvString = ""
        if(targetToken[0] is ' '):
            cnvString = '_' + targetToken[1]
        elif(targetToken[1] is ' '):
            cnvString = targetToken[0] + '_'
        else:
            cnvString = targetToken
        if cnvString in data_2mer:
            result = f(data_2mer[cnvString])
        result -= CUT_2MER
    elif len(targetToken) is 3:
        cnvString = ""
        if (targetToken[0] is ' ' and targetToken[2] is ' '):
            cnvString = '_' + targetToken[1] + '_'    
        elif(targetToken[0] is ' '):
            cnvString = '_' + targetToken[1:3]
        elif(targetToken[2] is ' '):
            cnvString = targetToken[0:2] + '_'
        else:
            cnvString = targetToken
        if cnvString in data_3mer:
            result = f(data_3mer[cnvString])
        result -= CUT_3MER
    return result

def main():
    show_kmer(data_1mer)

if __name__ == '__main__':
    main()
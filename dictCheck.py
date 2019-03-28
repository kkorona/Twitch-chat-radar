import json
import math
import matplotlib.pyplot as plt
from pprint import pprint

PATH_1MER = r'D:\Data\joongangdict\Joongang1merDicPy.json'
PATH_2MER = r'D:\Data\joongangdict\Joongang2merDicPy.json'
f = lambda x : math.log(x/2000)

with open(PATH_1MER,'r') as f_1mer:
    data_1mer = json.load(f_1mer)

with open(PATH_2MER,'r') as f_2mer:
    data_2mer = json.load(f_2mer)


def show_kmer(s_mer):
    global f
    show = []

    for merkey in s_mer:
        val = f(s_mer.get(merkey))
        show.append(val)

    show.sort()
    xl = range(0,len(show))

    plt.xlabel('log of frequency')
    plt.ylabel('# of people')
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
    elif len(targetToken) is 2:
        if targetToken in data_2mer:
            if(targetToken[0] is ' '):
                cnvString = '_' + targetToken[1]
            elif(targetToken[1] is ' '):
                cnvString = targetToken[0] + '_'
            else:
                cnvString = targetToken
            result = f(data_2mer[cnvString])
    else:
        result = 0
    return result

def main():
    show_kmer(data_2mer)

if __name__ == '__main__':
    main()
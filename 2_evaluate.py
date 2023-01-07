import os
import numpy as np
import pandas as pd
from ast import literal_eval
import editdistance


def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


if __name__=="__main__":
    path = './DATA/output/'
    files = os.listdir(path)
    files.sort()
    #print(jaccard(['a', 'b', 'c'], ['b', 'c', 'd']))
    #exit()

    ent = 0 
    cor = 0

    for afile in files[:]:
        data = pd.read_csv(path + afile)
        if not data.empty:
            print(afile, data['location'].values[0])
            #if editdistance.eval(literal_eval(data['location'].values[0]), literal_eval("['Sanghyeon', 'Seongbok', 'Suji-gu Office', 'Dongcheon', 'Migeum', 'Jeongja', 'Pangyo']")) < float(len(literal_eval(data['location'].values[0]))/2):
            if jaccard(literal_eval(data['location'].values[0]), literal_eval("['Sanghyeon', 'Seongbok', 'Suji-gu Office', 'Dongcheon', 'Migeum', 'Jeongja', 'Pangyo']")) > 0.4:
                cor += 1
                ent += 1
            else:
                ent += 1
    print(cor/ent)
    print(cor, ent)

import os
import sys
from dtw import *
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from scipy import integrate
from scipy.signal import medfilt

from src.Data_Processor import *

from scipy import signal

from numpy import random

from src.detect_peaks import detect_peaks



if __name__=='__main__':

    sp = Sensor_Processor()
    rp = Ref_Processor()
    #print([1, 1], np.matmul([1, 1], sp.rotation_matrix(30, mAxis='twoD')))
    #print(rp.calc_angle([0, 0], [-1, -1], np.matmul([1, 1], sp.rotation_matrix(30, mAxis='twoD'))))
    #print(rp.calc_angle([0, 0], [-1, -1], np.matmul([1, 1], sp.rotation_matrix(-30, mAxis='twoD'))))
    #print(rp.calc_angle([0, 0], [2.220446049250313e-16, 2.220446049250313e-16], [5.176899999845773, 5.322399999946356]))
    print(rp.calc_angle([0, 0], [2, 2], [5.176899999845773, 5.322399999946356]))
    exit()
    
    for i in range(1, 20):
        rot = random.randint(-80, 80)
        print(rp.calc_angle([0, 0], [0.000001, 1], np.matmul([-1, 0.000001], sp.rotation_matrix(rot, mAxis='twoD'))), rot)
        #val1x = random.randint(-5, 5)
        #val1y = random.randint(-5, 5)
        #val2x = random.randint(-5, 5)
        #val2y = random.randint(-5, 5)
        ##print(i, rp.calc_angle([0, 0], [1, 1], [-1, -i]), '-ac')
        ##print(i, rp.calc_angle([0, 0], [1, 1], [-i, -1]), '+ac')
        ##print(i, rp.calc_angle([0, 0], [-1, -i], [1, 1]), '+ac')
        ##print(i, rp.calc_angle([0, 0], [-i, -1], [1, 1]), '-ac')
        #print((val1x, val1y), (val2x, val2y), rp.calc_angle([0, 0], [val1x, val1y], [val2x, val2y]))


    exit()
    print(rp.calc_angle([0, 0], [1, 1], [-3, -1]), '+ ac')
    print(rp.calc_angle([0, 0], [1, 1], [-2, -1]), '+ ac')


    print(rp.calc_angle([0, 0], [1, 1], [-2, -1]), '+ ac')
    print(rp.calc_angle([0, 0], [1, 1], [-2, -1]), '+ ac')
    #print(rp.calc_angle([0, 0], [1, -1], [2, 1]), )
    #print(rp.calc_angle([0, 0], [-1, -1], [2, 1]), )
    exit()


    








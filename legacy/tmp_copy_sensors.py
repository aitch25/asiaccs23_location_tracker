import os
import sys
from dtw import *
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from scipy import integrate
from scipy.signal import medfilt

from sklearn.mixture import GaussianMixture as GMM
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA

from multiprocessing import Process

#sys.path.insert(0, "./class/")
#import src.Sensor_Processor as sproc
from src.Data_Processor import *
import src.Data_Loader as dl
#import Path_Analyzer as pana

from scipy import signal
from statsmodels.tsa.seasonal import seasonal_decompose

from numpy import random
from time import sleep

def flip_signals(mData):
    mData = -mData[::-1]

    return mData



if __name__=='__main__':

    sbds_lst = [52, 54, 55, 56, 57, 58, 59, 61, 63, 64, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80, 82, 94, 96, 98, 99, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 114, 115, 116, 117, 118, 119, 120, 121, 123, 128, 129, 130, 131, 132, 133, 134, 135, 136, 139, 140, 141, 142, 143, 144, 145, 146, 147, 149, 153, 154, 155, 156, 157, 159, 160, 161, 163, 165, 170, 171, 172, 176, 179, 182, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203]

    subway_paths, subway_paths_dic, _, _ = dl.Data_Loader().get_data()

    outpath = './DATA/sensors/prep/'

    for i, idx in enumerate(sbds_lst):
        path = '/home/hugh/DEV/ext_mem/ACMCCS/Crawl_OSM/' + subway_paths[idx] # 2, 5, 6, 8 
        start, end = subway_paths_dic[subway_paths[idx]] # 2, 5, 6, 8 
        print(idx, path, start, end)
        
        accl = pd.read_csv(path + 'accelerometer.csv')
        gyro = pd.read_csv(path + 'gyroscope.csv')
        magt = pd.read_csv(path + 'magneticfield.csv')

        randval1 = np.random.randint(-5, 5)
        randval2 = np.random.randint(-5, 5)
        accl = accl[start+randval1:end+randval2].reset_index()
        gyro = gyro[start+randval1:end+randval2].reset_index() 
        magt = magt[start+randval1:end+randval2].reset_index() 
        accl = accl.drop(columns=['index'])
        gyro = gyro.drop(columns=['index'])
        magt = magt.drop(columns=['index'])

        if 'sensordata' in subway_paths[idx]:
            #print('if', subway_paths[idx])
            accl['x'] = flip_signals(accl['x'].values)
            accl['y'] = flip_signals(accl['y'].values)
            accl['z'] = flip_signals(accl['z'].values)
            
            gyro['x'] = flip_signals(gyro['x'].values)
            gyro['y'] = flip_signals(gyro['y'].values)
            gyro['z'] = flip_signals(gyro['z'].values)
            
            magt['x'] = flip_signals(magt['x'].values)
            magt['y'] = flip_signals(magt['y'].values)
            magt['z'] = flip_signals(magt['z'].values)
            

        if '판교_상현' in subway_paths[idx]:
            os.system('mkdir ' + outpath + 'sensordata_{}_{}/'.format(str('%03d' % i), 'Pangyo_Sanghyeon'))

            accl.to_csv(outpath + 'sensordata_{}_{}/'.format(str('%03d' % i), 'Pangyo_Sanghyeon') + 'accelerometer.csv', index=False)
            gyro.to_csv(outpath + 'sensordata_{}_{}/'.format(str('%03d' % i), 'Pangyo_Sanghyeon') + 'gyroscope.csv', index=False)
            magt.to_csv(outpath + 'sensordata_{}_{}/'.format(str('%03d' % i), 'Pangyo_Sanghyeon') + 'magneticfield.csv', index=False)
        else:
            os.system('mkdir ' + outpath + 'sensordata_{}_{}/'.format(str('%03d' % i), 'Sanghyeon_Pangyo'))

            accl.to_csv(outpath + 'sensordata_{}_{}/'.format(str('%03d' % i), 'Sanghyeon_Pangyo') + 'accelerometer.csv', index=False)
            gyro.to_csv(outpath + 'sensordata_{}_{}/'.format(str('%03d' % i), 'Sanghyeon_Pangyo') + 'gyroscope.csv', index=False)
            magt.to_csv(outpath + 'sensordata_{}_{}/'.format(str('%03d' % i), 'Sanghyeon_Pangyo') + 'magneticfield.csv', index=False)





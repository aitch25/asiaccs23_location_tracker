import os
import sys
import numpy as np
import pandas as pd
from time import sleep 
import matplotlib.pyplot as plt

from copy import deepcopy

from scipy import integrate
from scipy.signal import medfilt, butter, filtfilt

from src.detect_peaks import detect_peaks

from dtw import *

from scipy.spatial import distance
from sklearn.preprocessing import MinMaxScaler

from random import randint



class Sensor_Processor:

    def butter_lowpass_filter(self, data, cutoff=1, fs=20, order=2):
        nyq= 0.5*fs
        normal_cutoff=cutoff/nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y=filtfilt(b, a, data)
        return y


    def get_move_moment_idx(self, mData, mWin_size, mThd):
        oOffset = int(mWin_size/2)
    
        oData_diff = np.append([0], np.diff(mData))

        oIdx = list(range(0, oOffset))

        for i in range(oOffset, len(mData)-oOffset):
            if mData[i-oOffset:i+oOffset].std() < mThd:
                oIdx.append(i)

        oIdx.extend(list(range(len(oIdx), len(oIdx)+oOffset)))

        return oIdx 


    def get_trace_from_sensor(self, mData, mBias):
        oAngle_weight = 3.33333333
    
        for _ in range(10):
            oData = medfilt(mData, 205)

        return (integrate.cumtrapz(oData - np.median(oData) - float(mBias)) * oAngle_weight)
    


    def get_2d_path(self, mHeading):
        oDead_reckoning = list()

        for head in zip(mHeading):
            oValocity = [1, 0, 0]
            oDead_reckoning.append(np.matmul(self.rotation_matrix(head, 'z'), oValocity))

        oDead_reckoning = np.transpose(oDead_reckoning)

        x_pnt = integrate.cumtrapz(oDead_reckoning[0])
        y_pnt = integrate.cumtrapz(oDead_reckoning[1])
        z_pnt = integrate.cumtrapz(oDead_reckoning[2])

        return x_pnt, y_pnt
    
   
    def rotation_matrix(self, mAngle, mAxis):
        angle = np.deg2rad(mAngle)
        
        if mAxis == 'x':
            oRot = [ [1,          0,           0],
                    [0, np.cos(angle), -np.sin(angle)],
                    [0, np.sin(angle),  np.cos(angle)]
                    ]
        
        elif mAxis == 'y':
            oRot = [ [np.cos(angle),  0, np.sin(angle)],
                    [0,           1,          0],
                    [-np.sin(angle), 0, np.cos(angle)]
                    ]
        
        elif mAxis == 'z':
            oRot = [ [np.cos(angle), -np.sin(angle), 0],
                    [np.sin(angle),  np.cos(angle), 0],
                    [0,            0,          1]
                    ]
        
        
        elif mAxis == 'twoD':
            oRot = [ [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle),  np.cos(angle)]
                    ]
        
        return oRot


    def sensor_rotation(self, mData, mAxis):

        oAng = list()

        oSVec = [np.finfo(float).eps, -9.8]

        for i in range(mData.shape[0]):

            if mAxis=='y':
                oAng.append(self.calc_angle_for_sensor([0, 0], [mData['x'].values[i], mData['z'].values[i]], oSVec))
            elif mAxis=='x':
                oAng.append(self.calc_angle_for_sensor([0, 0], [mData['y'].values[i], mData['z'].values[i]], oSVec))


        return np.array(oAng)
    
    def sensor_compensation(self, mData, mAngs, mAxis):
        oRet = list()
        for i in range(mData.shape[0]):
            oVec = (
                        mData['x'].values[i],
                        mData['y'].values[i],
                        mData['z'].values[i]
                   )
            oRet.append(np.matmul(oVec, self.rotation_matrix(mAngs[i], mAxis=mAxis)))
        

        oRet = np.array(oRet).T
        return pd.DataFrame({'x':oRet[0], 'y':oRet[1], 'z':oRet[2]})


    def find_stops(self, mData, mWin_size=50):
        oOffset = int(mWin_size/2)
    
        oVals = [0] * oOffset
    
        for i in range(oOffset, len(mData)-oOffset):
            oVals.append(mData[i-oOffset:i+oOffset].std())
    
        oVals.extend([0]*oOffset)
    
        oStops = list(detect_peaks(oVals, mpd=2400, valley=True, edge='both', show=False))
    
        return oStops
    
    def split_path(self, mData, mSplit_points, mMin_intv=1200):
    
        oData = list()
        for i in range(len(mSplit_points)-1):
            oPart = mData[mSplit_points[i]:mSplit_points[i+1]]
    
            if oPart.shape[0] > mMin_intv:
                oData.append(mData[mSplit_points[i]:mSplit_points[i+1]])
    
        return oData

    def calc_angle_for_sensor(self, mIntSec, mVec1, mVec2):
    
        mVec1[0] = mVec1[0] - mIntSec[0]
        mVec1[1] = mVec1[1] - mIntSec[1]
    
        mVec2[0] = mVec2[0] - mIntSec[0]
        mVec2[1] = mVec2[1] - mIntSec[1]

        mVec1[0] += np.finfo(float).eps
        mVec1[1] += np.finfo(float).eps
        mVec2[0] += np.finfo(float).eps
        mVec2[1] += np.finfo(float).eps
    
    
        if (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 1, 1
            v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] >=0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 2, 2
            v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 3, 3
            v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 4, 4
            v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 1, 2
            v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 2, 1
            v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 1, 3
            v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
            if retAng > 180:
                retAng = -(360-retAng)
    
    
        elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 3, 1
            v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng =(v2Ang - v1Ang)
            if retAng < -180:
                retAng = (360+retAng)
    
        elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 1, 4
            v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = -(360-(v2Ang - v1Ang))
    
        elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 4, 1
            v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = 360+(v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 2, 3
            v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 3, 2
            v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
            ##################################
    
        elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 2, 4
            v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
            if retAng > 180:
                retAng = -(360-retAng)
    
        elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 4, 2
            v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
            if retAng < -180:
                retAng = 360+retAng
    
    
        elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 3, 4
            v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 4, 3
            v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        if abs(retAng) == 180.0:
            retAng = 0.0
        elif retAng > 0:
            retAng = (180.0 - retAng)
        elif retAng < 0:
            retAng = -(180.0 + retAng)
    
        return retAng






class Ref_Processor:
    
    def calc_angle(self, mIntSec, mVec1, mVec2):
    
        mVec1[0] = mVec1[0] - mIntSec[0]
        mVec1[1] = mVec1[1] - mIntSec[1]
    
        mVec2[0] = mVec2[0] - mIntSec[0]
        mVec2[1] = mVec2[1] - mIntSec[1]

        retAng = (np.pi-(np.math.atan2(np.linalg.det([mVec1, mVec2]), np.dot(mVec1, mVec2)) % (np.pi*2))) * (180 / np.pi)

        return retAng
    
    def get_continuous_sequence(self, mVec):
        mVec = mVec[['src_x', 'src_y', 'dst_x', 'dst_y']].drop_duplicates()
        X1 = mVec['src_x'].values * 10000
        Y1 = mVec['src_y'].values * 10000
        X2 = mVec['dst_x'].values * 10000
        Y2 = mVec['dst_y'].values * 10000

        oAd_seq = [0]
        for i in range(mVec.shape[0]-1):
            oDist = distance.euclidean((X1[i], Y1[i]), (X2[i], Y2[i])) * 2

            oZero_pad = [oAd_seq[-1] for _ in range(round(oDist))] 
            oAd_seq.extend(oZero_pad)
            oAd_seq.append(oAd_seq[-1] + float(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[i+1], Y2[i+1]])))

        return medfilt(np.array(oAd_seq), 25) 




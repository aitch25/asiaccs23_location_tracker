import os
import sys
import numpy as np
import pandas as pd
from time import sleep 
import matplotlib.pyplot as plt

from copy import deepcopy

from scipy import integrate
from scipy.signal import medfilt, butter, filtfilt


import src.Path_Analyzer as pana
from src.detect_peaks import detect_peaks

from dtw import *

from scipy.spatial import distance
from sklearn.preprocessing import MinMaxScaler

from random import randint



class Sensor_Processor:

    def meanfilt (self, x, k):
        """Apply a length-k mean filter to a 1D array x.
        Boundaries are extended by repeating endpoints.
        """
    
        assert k % 2 == 1, "Mean filter length must be odd."
        assert x.ndim == 1, "Input must be one-dimensional."
    
        k2 = (k - 1) // 2
        y = np.zeros ((len (x), k), dtype=x.dtype)
        y[:,k2] = x
        for i in range (k2):
            j = k2 - i
            y[j:,i] = x[:-j]
            y[:j,i] = x[0]
            y[:-j,-(i+1)] = x[j:]
            y[-j:,-(i+1)] = x[-1]
        return np.mean (y, axis=1)

    def butter_lowpass_filter(self, data, cutoff=1, fs=20, order=2):
        nyq= 0.5*fs
        normal_cutoff=cutoff/nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y=filtfilt(b, a, data)
        return y

    
    def extract_path_num(self, mData, mWin_size, mThd):
        oOffset = int(mWin_size/2)
    
        oData_diff = np.append([0], np.diff(mData))

        oIdx = list(range(0, oOffset))

        for i in range(oOffset, len(mData)-oOffset):
            if mData[i-oOffset:i+oOffset].std() < mThd:
                oIdx.append(i)

        oIdx.extend(list(range(len(oIdx), len(oIdx)+oOffset)))

        return oIdx 



    def get_move_moment_idx(self, mData, mWin_size, mThd):
        oOffset = int(mWin_size/2)
    
        #oData = np.append([0], np.diff(mData[:oOffset]))
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

        pa = pana.Path_Analyzer()

        for i in range(mData.shape[0]):

            if mAxis=='y':
                oAng.append(pa.calc_angle([0, 0], [mData['x'].values[i], mData['z'].values[i]], oSVec))
            elif mAxis=='x':
                oAng.append(pa.calc_angle([0, 0], [mData['y'].values[i], mData['z'].values[i]], oSVec))


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
        #oStops = list(detect_peaks(oVals, mpd=2400, valley=True, edge='both', show=True))
        #oStops = [0] + oStops + [mData.shape[0]]
    
        return oStops
    
    def split_path(self, mData, mSplit_points, mMin_intv=1200):
    
        oData = list()
        for i in range(len(mSplit_points)-1):
            oPart = mData[mSplit_points[i]:mSplit_points[i+1]]
    
            if oPart.shape[0] > mMin_intv:
                oData.append(mData[mSplit_points[i]:mSplit_points[i+1]])
    
        return oData







class Ref_Processor:
    def mod(self, a, b):
        return float(a) % float(b)


        oTimegap = pd.DataFrame()
        for i in range(mTimegap.shape[0]):
            for j in range(i, mTimegap.shape[0]):
                if mTimegap[i:j+1]['mins'].sum()>=oMax_minutes: 
                    oTmp = mTimegap[i:j+1]
                    oTmp['id'] = mTimegap.values[i][0] + ':' + mTimegap.values[j][1]
                    if oTimegap.empty:
                        oTimegap = oTmp.copy()
                    else:
                        oTimegap = oTimegap.append(oTmp)
                    break

        return oTimegap


    def get_station_timegap_ngram(self, mTimegap, mLen=3):

        mTimegap['line'] = mTimegap['filename'].copy()
        mTimegap['line'] = mTimegap['line'].replace('line_sbds', '신분당선')

        oTimegap = pd.DataFrame()
        for i in range(mTimegap.shape[0]-(mLen-1)):
            oTmp = mTimegap[i:i+mLen]
            oTmp['id'] = mTimegap.values[i][0] + ':' + mTimegap.values[i+(mLen-1)][1]
            if oTimegap.empty:
                oTimegap = oTmp.copy()
            else:
                oTimegap = oTimegap.append(oTmp)
            #break

        return oTimegap

    def get_station_seq(self, mStation_seq, mLine):
        mStation_seq.sort()
        if len(mStation_seq) == 2:
            return [(mStation_seq[0], mStation_seq[1])]
        elif len(mStation_seq)>2:
            return [(mStation_seq[0], mStation_seq[1]), (mStation_seq[1], mStation_seq[2])]



    def get_paths(self, mSrc, mDst, mLine, mPath_len=5):
    
        #print(os.system('pwd'))
        oTimegap_path = './input/timegap/subways/'
        oTimegap_files = os.listdir(oTimegap_path)
        #print(oTimegap_files)
        #exit()
        oTimegap_files.sort()
    
        oCandidate_ans = list()
        for tg_file in oTimegap_files[:]:
            #print('a:t', mLine, tg_file)
            if mLine in tg_file:
                atimegap = pd.read_csv(oTimegap_path + tg_file)
                #print('a:t', atimegap)
                atimegap['filename'] = tg_file.split('.')[0]
                atimegap = atimegap[['srcs', 'filename']].append(atimegap[['dsts', 'filename']].rename(columns={'dsts':'srcs'})[-1:])
                atimegap = atimegap.reset_index()[['srcs', 'filename']].rename(columns={'srcs':'stations'})
                atimegap['index'] = atimegap.index
                atimegap = atimegap[['index', 'stations', 'filename']]
    
                #print('src', tg_file, mSrc, atimegap['stations'].values)
                #print('dst', tg_file, mDst, atimegap['stations'].values)
    
                if (mSrc in atimegap['stations'].values) & (mDst in atimegap['stations'].values):
                    src = atimegap[atimegap['stations']==mSrc]['index'].values
                    dst = atimegap[atimegap['stations']==mDst]['index'].values
                    station_idx = list()
                    [station_idx.append(s) for s in src]
                    [station_idx.append(d) for d in dst]
    
                    idxs = self.get_station_seq(station_idx, atimegap)
                    for idx in idxs:
                        at = atimegap[idx[0]:idx[1]+1]['stations'].values
                        at += mLine
                        oCandidate_ans.append(list(at))
    
        #oCandidate_ans.sort(key=len)
        #return np.unique(oCandidate_ans)
        oCandidate_ans = np.unique(oCandidate_ans)
        oCandidate_ans = sorted(oCandidate_ans, key=len)
        #print('candi', oCandidate_ans)
    
        if len(oCandidate_ans)==0:
            return list()
        elif type(oCandidate_ans[0])==list:
            for oc in oCandidate_ans:
                if len(oc)==mPath_len:
                    return oc
                elif (len(oc)-1)==mPath_len:
                    return oc
                elif (len(oc)+1)==mPath_len:
                    return oc
                elif (len(oc)-2)==mPath_len:
                    return oc
                elif (len(oc)+2)==mPath_len:
                    return oc
                else:
                    return oCandidate_ans[0] # need to fix 220504
        else:
            return oCandidate_ans

    
    def calc_angle(self, mIntSec, mVec1, mVec2):
    
        mVec1[0] = mVec1[0] - mIntSec[0]
        mVec1[1] = mVec1[1] - mIntSec[1]
    
        mVec2[0] = mVec2[0] - mIntSec[0]
        mVec2[1] = mVec2[1] - mIntSec[1]

        retAng = (np.pi-(np.math.atan2(np.linalg.det([mVec1, mVec2]), np.dot(mVec1, mVec2)) % (np.pi*2))) * (180 / np.pi)

        #mVec1[0] += np.finfo(float).eps
        #mVec1[1] += np.finfo(float).eps
        #mVec2[0] += np.finfo(float).eps
        #mVec2[1] += np.finfo(float).eps

    
        #if (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 1, 1
        #    v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #elif (mVec1[0] <= 0) & (mVec1[1] >=0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 2, 2
        #    v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 3, 3
        #    v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 4, 4
        #    v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 1, 2
        #    v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
        #    #retAng = mod(retAng, 360)
    
        #elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 2, 1
        #    v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 1, 3
        #    v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
        #    if retAng > 180:
        #        retAng = -(360-retAng)
    
    
        #elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 3, 1
        #    v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng =(v2Ang - v1Ang)
        #    if retAng < -180:
        #        retAng = (360+retAng)
    
        #elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 1, 4
        #    v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = -(360-(v2Ang - v1Ang))
    
        #elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 4, 1
        #    v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = 360+(v2Ang - v1Ang) 
    
        #elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 2, 3
        #    v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 3, 2
        #    v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #    ##################################
    
        #elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 2, 4
        #    v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
        #    if retAng > 180:
        #        retAng = -(360-retAng)
    
        #elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 4, 2
        #    v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
        #    if retAng < -180:
        #        retAng = 360+retAng
    
    
        #elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 3, 4
        #    v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 4, 3
        #    v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
        #    v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
        #    retAng = (v2Ang - v1Ang)
    
        #if abs(retAng) == 180.0:
        #    retAng = 0.0
        #elif retAng > 0:
        #    retAng = (180.0 - retAng)
        #elif retAng < 0:
        #    retAng = -(180.0 + retAng)


        return retAng
    
    

    def adjusting_sig_pos(self, mStraights, mVec):

        #oVec = mVec.copy() #pd.Series(mVec)

        oStraights_pair = list()
        for i in range(len(mStraights)-1):
            if (mStraights[i]+mStraights[i+1]) == 1:
                oStraights_pair.append(i+1)

        oStraights_on = list() 
        oStraight_pair = list()
        for straight in oStraights_pair[1:-1]:
            if len(oStraight_pair) < 2:
                oStraight_pair.append(straight)
            else:
                oStraights_on.append(oStraight_pair)
                oStraight_pair = list()


        for straight in oStraights_on:
            if mVec[straight[0]] - mVec[straight[1]] > 180.:
                oMin = mVec[straight[1]] + 360
                oMax = mVec[straight[0]]

                if oMin < oMax:
                    oScaler = MinMaxScaler((oMin, oMax))
                elif oMin > oMax:
                    oScaler = MinMaxScaler((oMax, oMin))
                else:
                    oScaler = MinMaxScaler((oMin, oMin+0.00000000001))

                #print(oMin, oMax)
                mVec[straight[0]:straight[1]] = oScaler.fit_transform(np.array(mVec[straight[0]:straight[1]]).reshape(-1, 1)).reshape(1, -1)[0]
                mVec[straight[1]:] = [val+360. for val in mVec[straight[1]:]] 

            elif mVec[straight[1]] - mVec[straight[0]] > 180.:
                oMin = mVec[straight[0]]
                oMax = mVec[straight[1]] - 360
                if oMin < oMax:
                    oScaler = MinMaxScaler((oMin, oMax))
                elif oMin > oMax:
                    oScaler = MinMaxScaler((oMax, oMin))
                else:
                    oScaler = MinMaxScaler((oMin, oMin+0.00000000001))

                #print(mVec[straight[0]:straight[1]])
                #print(oScaler.fit_transform(np.array(mVec[straight[0]:straight[1]]).reshape(-1, 1)).reshape(1, -1))
                mVec[straight[0]:straight[1]] = oScaler.fit_transform(np.array(mVec[straight[0]:straight[1]]).reshape(-1, 1)).reshape(1, -1)[0]

                mVec[straight[1]:] = [val-360. for val in mVec[straight[1]:]] 

        return mVec


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
            #oAd_seq.append(oAd_seq[-1] + float(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[i+1], Y2[i+1]])))
            oAd_seq.append(oAd_seq[-1] + float(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[i+1], Y2[i+1]])))

        return medfilt(np.array(oAd_seq), 25) 



    
    def search_path(self, mPPath, mFPath, mErr):
        # mPPath : Partial Path
        # mFPath : Full Path
    
        #oPPath = mPPath.split('>')
        oPPath = mPPath.copy()
        oFPath = mFPath.copy()
    
        oRecursive_Path = dict()
    
        for i, angle in enumerate(oPPath):
            oRecursive_Path[str(i) + '_loop'] = list()
            for j in list(range(len(oFPath))):
                for k, angle_map in enumerate(oFPath[j]):
                    if (float(angle) < (float(angle_map.split(':')[0])+float(mErr))) & (float(angle) > (float(angle_map.split(':')[0])-float(mErr))):
                        #print(angle, angle_map)
                        oRecursive_Path[str(i) + '_loop'].append([j, k])
    
        
        oCur_Path = list()
        oCur_Filtered = list()
    
        for pair in oRecursive_Path['0_loop']:
            oCur_Path.append(pair)
        
        for i in range(1, len(oPPath)):
            for pair1 in oCur_Path:
                if len(pair1) == (i+1):
                    oCur_Filtered.append(pair1)
    
            for pair1 in oCur_Filtered:
                for pair2 in oRecursive_Path[str(i) + '_loop']:
                    oCur_Path2 = list()
                    if (float(mFPath[pair1[-2]][pair2[1]].split(':')[0])==np.inf) & ((pair1[-1]==pair2[0]) & (pair1[-2]!=pair2[1])) & (str(oFPath[pair1[-2]][pair1[-1]].split(':')[1])[1] != (str(oFPath[pair2[0]][pair2[1]].split(':')[1])[0])):
                        for p1 in pair1:
                            oCur_Path2.append(p1)
                        oCur_Path2.append(pair2[1])
                        oCur_Path.append(oCur_Path2)
    
    
        oRet_list = list()
        for pl in oCur_Path:
            if len(pl) == len(oPPath)+1:
                oRet_list.append(pl)
    
        
        if len(oRet_list):
            return oRet_list
        else:
            return list()

    
    def plot_graph(self, mData, mAdj_mat, mRet_list, mType):
    
        if mType == 'all':
            for i, rl in enumerate(mRet_list):
                print(i, rl)
                for i in range(len(rl)-1):
                    print(mAdj_mat[rl[i]][rl[i+1]])
                
                oData_plot = pd.DataFrame()
                oData_plot = oData_plot.append(mData.loc[rl])
    
                plt.figure(figsize=(20, 20))
                plt.plot([oData_plot['src_x'], oData_plot['dst_x']], [oData_plot['src_y'], oData_plot['dst_y']], '-', linewidth=5)
    
                plt.grid(True)
                plt.savefig('./plot_vir.png')
                #plt.show()
    
                sleep(1)
    
    
        elif mType == 'origin':
            plt.figure(figsize=(20, 20))
            plt.plot([mData['src_x'], mData['dst_x']], [mData['src_y'], mData['dst_y']], '-', linewidth=5)
    
            plt.grid(True)
            plt.savefig('./plot_vir.png')
            #plt.show()
    
    
        else:
            oData_plot = mData.loc[mRet_list[int(mType)]]
    
            for i in range(len(mRet_list[int(mType)])-1):
                print(mAdj_mat[mRet_list[int(mType)][i]][mRet_list[int(mType)][i+1]])
    
    
            plt.figure(figsize=(20, 20))
            plt.plot([oData_plot['src_x'], oData_plot['dst_x']], [oData_plot['src_y'], oData_plot['dst_y']], '-', linewidth=5)
    
            plt.grid(True)
            plt.savefig('./plot_vir.png')
            #plt.show()
    
    
    def get_angle_vec(self, mAdj_mat_o):
    
        oAng_vec = list()
        for angs in mAdj_mat_o:
            oAng_vec.extend(angs)
            oAng_vec = list(set(oAng_vec))
    
        for i in range(len(oAng_vec)):
            oAng_vec[i] = float(oAng_vec[i].split(':')[0])
    
        oAng_hist = list()
        for angs in oAng_vec:
            if angs != np.inf:
                oAng_hist.append(angs)
    
    
        return oAng_hist








